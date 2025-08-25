import pytest
from datetime import date, timedelta
from app.service.property import (
    list_properties,
    find_conflicts,
    check_availability,
    create_property,
    delete_property_by_id,
)
from app.db.schema import PropertyCreate


from app.tests.conftest import _mk_property, _mk_reservation


def test_list_properties__filtros_exatos(db_session):
    p1 = _mk_property(db_session, address_city="Florianópolis", address_state="SC", address_neighborhood="Centro")
    p2 = _mk_property(db_session, address_city="São Paulo", address_state="SP", address_neighborhood="Bela Vista")


    res = list_properties(db_session, address_city="Florianópolis")
    assert [x.id for x in res] == [p1.id]

    res = list_properties(db_session, address_state="SP")
    assert [x.id for x in res] == [p2.id]


    res = list_properties(db_session, address_neighborhood="Centro")
    assert [x.id for x in res] == [p1.id]


def test_list_properties__capacidade_e_preco(db_session):
    _mk_property(db_session, capacity=2, price_per_night=300)
    p_ok = _mk_property(db_session, capacity=5, price_per_night=150)
    _mk_property(db_session, capacity=8, price_per_night=400)

    res = list_properties(db_session, capacity=4, price_per_night=200)
    assert [x.id for x in res] == [p_ok.id]


def test_find_conflicts(db_session):
    prop = _mk_property(db_session)
    r1 = _mk_reservation(
        db_session,
        property_id=prop.id,
        start_date=date(2025, 8, 10),
        end_date=date(2025, 8, 15),
    )

    conflicts = find_conflicts(db_session, prop.id, date(2025, 8, 12), date(2025, 8, 13))
    assert conflicts == [r1.id]

    conflicts = find_conflicts(db_session, prop.id, date(2025, 8, 16), date(2025, 8, 18))
    assert conflicts == []


def test_check_availability__datas_iguais_gera_409(db_session):
    prop = _mk_property(db_session)
    with pytest.raises(Exception) as ex:
        check_availability(
            db_session,
            property_id=prop.id,
            start_date=date(2025, 8, 22),
            end_date=date(2025, 8, 22),
            guests_quantity=2,
        )
    # 409 ????????????
    assert "data de saída" in str(ex.value).lower()


def test_check_availability__prop_inexistente_gera_404(db_session):
    with pytest.raises(Exception) as ex:
        check_availability(
            db_session,
            property_id=9999,
            start_date=date(2025, 8, 22),
            end_date=date(2025, 8, 23),
            guests_quantity=2,
        )
    assert "propriedade não encontrada" in str(ex.value).lower()


def test_check_availability__capacidade_insuficiente_gera_409(db_session):
    prop = _mk_property(db_session, capacity=2)
    with pytest.raises(Exception) as ex:
        check_availability(
            db_session,
            property_id=prop.id,
            start_date=date(2025, 8, 22),
            end_date=date(2025, 8, 23),
            guests_quantity=3,
        )
    assert "capacidade insuficiente" in str(ex.value).lower()


def test_check_availability__conflito_reserva_gera_409(db_session):
    prop = _mk_property(db_session)
    _mk_reservation(
        db_session,
        property_id=prop.id,
        start_date=date(2025, 8, 22),
        end_date=date(2025, 8, 25),
    )
    with pytest.raises(Exception) as ex:
        check_availability(
            db_session,
            property_id=prop.id,
            start_date=date(2025, 8, 23),
            end_date=date(2025, 8, 24),
            guests_quantity=2,
        )
    assert "período indisponível" in str(ex.value).lower()


def test_check_availability__ok_retorna_propriedade(db_session):
    prop = _mk_property(db_session, capacity=4)
    _mk_reservation(
        db_session,
        property_id=prop.id,
        start_date=date(2025, 8, 10),
        end_date=date(2025, 8, 12),
    )
    res = check_availability(
        db_session,
        property_id=prop.id,
        start_date=date(2025, 8, 13),
        end_date=date(2025, 8, 15),
        guests_quantity=3,
    )
    assert [x.id for x in res] == [prop.id]


def test_create_property__persiste(db_session):
    payload = PropertyCreate(
        title="Casa Nova",
        address_street="Rua Beta",
        address_number="55",
        address_neighborhood="Centro",
        address_city="Florianópolis",
        address_state="SC",
        country="Brasil",
        rooms=2,
        capacity=4,
        price_per_night=200,
    )
    from app.service.property import create_property
    obj = create_property(db_session, payload)
    assert obj.id is not None
    assert obj.title == "Casa Nova"


def test_delete_property_by_id(db_session):
    p = _mk_property(db_session)
    ok = delete_property_by_id(db_session, p.id)
    assert ok is True

    ok2 = delete_property_by_id(db_session, p.id)
    assert ok2 is False
