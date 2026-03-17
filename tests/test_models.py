"""
Unit tests for data models
"""

import pytest
from core.models import (
    Relationship, Cardinality, CrossFilterDirection,
    DAXMeasure, DAXComplexity,
    Table, Column, ColumnDataType, TableType,
    DataModel
)


class TestRelationship:
    """Tests for Relationship model"""

    def test_relationship_creation(self):
        """Test creating a relationship with all fields"""
        rel = Relationship(
            from_table="Ventas",
            from_column="ClienteID",
            to_table="Clientes",
            to_column="ID",
            cardinality=Cardinality.MANY_TO_ONE,
            cross_filter_direction=CrossFilterDirection.SINGLE,
            is_active=True
        )

        assert rel.from_table == "Ventas"
        assert rel.to_table == "Clientes"
        assert rel.cardinality == Cardinality.MANY_TO_ONE
        assert rel.cross_filter_direction == CrossFilterDirection.SINGLE
        assert rel.is_active is True

    def test_relationship_from_strings(self):
        """Test creating relationship from string values"""
        rel = Relationship(
            from_table="Ventas",
            from_column="ProductoID",
            to_table="Productos",
            to_column="ID",
            cardinality="*:1",  # String input
            cross_filter_direction="single",  # String input
        )

        assert rel.cardinality == Cardinality.MANY_TO_ONE
        assert rel.cross_filter_direction == CrossFilterDirection.SINGLE

    def test_cardinality_from_parts(self):
        """Test Cardinality.from_parts method"""
        card = Cardinality.from_parts("many", "one")
        assert card == Cardinality.MANY_TO_ONE

        card = Cardinality.from_parts("one", "many")
        assert card == Cardinality.ONE_TO_MANY

        card = Cardinality.from_parts("one", "one")
        assert card == Cardinality.ONE_TO_ONE

        card = Cardinality.from_parts("many", "many")
        assert card == Cardinality.MANY_TO_MANY

    def test_relationship_properties(self):
        """Test relationship computed properties"""
        # Bidirectional relationship
        rel_bidir = Relationship(
            from_table="Tabla1",
            from_column="Col1",
            to_table="Tabla2",
            to_column="Col2",
            cardinality=Cardinality.ONE_TO_MANY,
            cross_filter_direction=CrossFilterDirection.BOTH
        )
        assert rel_bidir.is_bidirectional is True

        # Many-to-many relationship
        rel_m2m = Relationship(
            from_table="Tabla1",
            from_column="Col1",
            to_table="Tabla2",
            to_column="Col2",
            cardinality=Cardinality.MANY_TO_MANY,
            cross_filter_direction=CrossFilterDirection.SINGLE
        )
        assert rel_m2m.is_many_to_many is True

    def test_relationship_to_dict(self):
        """Test relationship serialization"""
        rel = Relationship(
            from_table="Ventas",
            from_column="ClienteID",
            to_table="Clientes",
            to_column="ID",
            cardinality=Cardinality.MANY_TO_ONE,
            cross_filter_direction=CrossFilterDirection.SINGLE
        )

        rel_dict = rel.to_dict()

        assert rel_dict['from_table'] == "Ventas"
        assert rel_dict['cardinality'] == "*:1"
        assert rel_dict['is_bidirectional'] is False
        assert rel_dict['is_many_to_many'] is False

    def test_relationship_str(self):
        """Test string representation"""
        rel = Relationship(
            from_table="Ventas",
            from_column="ClienteID",
            to_table="Clientes",
            to_column="ID",
            cardinality=Cardinality.MANY_TO_ONE,
            cross_filter_direction=CrossFilterDirection.SINGLE
        )

        rel_str = str(rel)
        assert "Ventas.ClienteID" in rel_str
        assert "Clientes.ID" in rel_str
        assert "*:1" in rel_str


class TestDAXMeasure:
    """Tests for DAXMeasure model"""

    def test_dax_measure_creation(self):
        """Test creating a DAX measure"""
        measure = DAXMeasure(
            name="Total Ventas",
            expression="SUM(Ventas[Importe])",
            table="Ventas",
            description="Suma total de ventas"
        )

        assert measure.name == "Total Ventas"
        assert measure.expression == "SUM(Ventas[Importe])"
        assert measure.table == "Ventas"
        assert measure.expression_length > 0

    def test_dax_complexity_simple(self):
        """Test complexity calculation for simple measure"""
        measure = DAXMeasure(
            name="Total Ventas",
            expression="SUM(Ventas[Importe])",
            table="Ventas"
        )

        assert measure.complexity == DAXComplexity.LOW

    def test_dax_complexity_medium(self):
        """Test complexity calculation for medium measure"""
        measure = DAXMeasure(
            name="Ventas YTD",
            expression="CALCULATE(SUM(Ventas[Importe]), DATESYTD(Calendario[Fecha]))",
            table="Ventas"
        )

        assert measure.complexity in [DAXComplexity.MEDIUM, DAXComplexity.HIGH]

    def test_dax_complexity_high(self):
        """Test complexity calculation for complex measure"""
        complex_expr = """
        CALCULATE(
            SUMX(
                FILTER(
                    Ventas,
                    Ventas[Categoria] = "A"
                ),
                Ventas[Importe] * Ventas[Cantidad]
            ),
            ALL(Productos),
            USERELATIONSHIP(Ventas[Fecha], Calendario[Fecha])
        )
        """
        measure = DAXMeasure(
            name="Ventas Complejas",
            expression=complex_expr,
            table="Ventas"
        )

        assert measure.complexity in [DAXComplexity.HIGH, DAXComplexity.VERY_HIGH]

    def test_dax_function_detection(self):
        """Test detection of DAX functions"""
        measure = DAXMeasure(
            name="Test",
            expression="CALCULATE(SUM(Ventas[Importe]), FILTER(Productos, Productos[Tipo] = \"A\"))",
            table="Ventas"
        )

        assert 'CALCULATE' in measure.function_count
        assert 'FILTER' in measure.function_count
        assert 'SUM' in measure.function_count

    def test_dax_time_intelligence(self):
        """Test time intelligence detection"""
        measure = DAXMeasure(
            name="Ventas YTD",
            expression="TOTALYTD(SUM(Ventas[Importe]), Calendario[Fecha])",
            table="Ventas"
        )

        assert measure.has_time_intelligence is True

    def test_dax_context_transition(self):
        """Test context transition detection"""
        measure = DAXMeasure(
            name="Test Calculate",
            expression="CALCULATE(SUM(Ventas[Importe]), Productos[Categoria] = \"A\")",
            table="Ventas"
        )

        assert measure.uses_context_transition is True

    def test_dax_iterators(self):
        """Test iterator detection"""
        measure = DAXMeasure(
            name="Test Iterator",
            expression="SUMX(Ventas, Ventas[Cantidad] * Ventas[Precio])",
            table="Ventas"
        )

        assert measure.uses_iterators is True


class TestColumn:
    """Tests for Column model"""

    def test_column_creation(self):
        """Test creating a column"""
        col = Column(
            name="ClienteID",
            table="Ventas",
            data_type=ColumnDataType.INT64,
            is_key=True
        )

        assert col.name == "ClienteID"
        assert col.table == "Ventas"
        assert col.data_type == ColumnDataType.INT64
        assert col.is_key is True

    def test_column_full_name(self):
        """Test full column name property"""
        col = Column(
            name="Importe",
            table="Ventas",
            data_type=ColumnDataType.DOUBLE
        )

        assert col.full_name == "Ventas[Importe]"

    def test_calculated_column(self):
        """Test calculated column"""
        col = Column(
            name="ImporteTotal",
            table="Ventas",
            data_type=ColumnDataType.DOUBLE,
            is_calculated=True,
            expression="Ventas[Cantidad] * Ventas[PrecioUnitario]"
        )

        assert col.is_calculated is True
        assert col.expression is not None


class TestTable:
    """Tests for Table model"""

    def test_table_creation(self):
        """Test creating a table"""
        table = Table(
            name="Ventas",
            table_type=TableType.REGULAR
        )

        assert table.name == "Ventas"
        assert table.table_type == TableType.REGULAR
        assert table.column_count == 0

    def test_table_with_columns(self):
        """Test table with columns"""
        columns = [
            Column(name="ID", table="Ventas", data_type=ColumnDataType.INT64),
            Column(name="Importe", table="Ventas", data_type=ColumnDataType.DOUBLE),
            Column(name="Cantidad", table="Ventas", data_type=ColumnDataType.INT64)
        ]

        table = Table(
            name="Ventas",
            columns=columns
        )

        assert table.column_count == 3

    def test_table_get_column(self):
        """Test getting column by name"""
        columns = [
            Column(name="ID", table="Ventas", data_type=ColumnDataType.INT64),
            Column(name="Importe", table="Ventas", data_type=ColumnDataType.DOUBLE)
        ]

        table = Table(name="Ventas", columns=columns)

        col = table.get_column("Importe")
        assert col is not None
        assert col.name == "Importe"

        col_none = table.get_column("NoExiste")
        assert col_none is None


class TestDataModel:
    """Tests for DataModel"""

    def test_data_model_creation(self):
        """Test creating a data model"""
        model = DataModel()

        assert model.table_count == 0
        assert model.relationship_count == 0
        assert model.measure_count == 0

    def test_data_model_with_tables(self):
        """Test data model with tables"""
        tables = [
            Table(name="Ventas"),
            Table(name="Clientes"),
            Table(name="Productos")
        ]

        model = DataModel(tables=tables)

        assert model.table_count == 3

    def test_data_model_get_table(self):
        """Test getting table by name"""
        tables = [
            Table(name="Ventas"),
            Table(name="Clientes")
        ]

        model = DataModel(tables=tables)

        table = model.get_table("Ventas")
        assert table is not None
        assert table.name == "Ventas"

    def test_data_model_with_relationships(self):
        """Test data model with relationships"""
        relationships = [
            Relationship(
                from_table="Ventas",
                from_column="ClienteID",
                to_table="Clientes",
                to_column="ID",
                cardinality=Cardinality.MANY_TO_ONE,
                cross_filter_direction=CrossFilterDirection.SINGLE
            ),
            Relationship(
                from_table="Ventas",
                from_column="ProductoID",
                to_table="Productos",
                to_column="ID",
                cardinality=Cardinality.MANY_TO_ONE,
                cross_filter_direction=CrossFilterDirection.BOTH
            )
        ]

        model = DataModel(relationships=relationships)

        assert model.relationship_count == 2
        assert len(model.get_bidirectional_relationships()) == 1

    def test_data_model_table_relationships(self):
        """Test getting relationships for a specific table"""
        relationships = [
            Relationship(
                from_table="Ventas",
                from_column="ClienteID",
                to_table="Clientes",
                to_column="ID",
                cardinality=Cardinality.MANY_TO_ONE,
                cross_filter_direction=CrossFilterDirection.SINGLE
            ),
            Relationship(
                from_table="Ventas",
                from_column="ProductoID",
                to_table="Productos",
                to_column="ID",
                cardinality=Cardinality.MANY_TO_ONE,
                cross_filter_direction=CrossFilterDirection.SINGLE
            )
        ]

        model = DataModel(relationships=relationships)

        ventas_rels = model.get_table_relationships("Ventas")
        assert len(ventas_rels) == 2

        clientes_rels = model.get_table_relationships("Clientes")
        assert len(clientes_rels) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
