import pytest
from battery import Battery
from unittest.mock import Mock

@pytest.fixture
def charged_battery():
    return Battery(100)

@pytest.fixture
def partially_charged_battery():
    b = Battery(100)
    b.mCharge = 50
    return b

@pytest.fixture
def empty_battery():
    b = Battery(100)
    b.mCharge = 0
    return b

def describe_Battery():
    def test_initial_state():
        battery = Battery(100)
        assert battery.getCapacity() == 100
        assert battery.getCharge() == 100

    def describe_recharge():
        def test_normal_recharge(partially_charged_battery):
            assert partially_charged_battery.recharge(20) is True
            assert partially_charged_battery.getCharge() == 70
        
        def test_exceeds_capacity(partially_charged_battery):
            assert partially_charged_battery.recharge(60) is True
            assert partially_charged_battery.getCharge() == 100
        
        def test_negative_amount(partially_charged_battery):
            assert partially_charged_battery.recharge(-10) is False
            assert partially_charged_battery.getCharge() == 50
        
        def test_already_full(charged_battery):
            assert charged_battery.recharge(10) is False
            assert charged_battery.getCharge() == 100
        
        def test_monitor_notification(partially_charged_battery):
            monitor = Mock()
            partially_charged_battery.external_monitor = monitor
            partially_charged_battery.recharge(20)
            monitor.notify_recharge.assert_called_once_with(70)
    
    def describe_drain():
        def test_normal_drain(charged_battery):
            assert charged_battery.drain(30) is True
            assert charged_battery.getCharge() == 70
        
        def test_complete_drain(partially_charged_battery):
            assert partially_charged_battery.drain(60) is True
            assert partially_charged_battery.getCharge() == 0
        
        def test_negative_amount(charged_battery):
            assert charged_battery.drain(-10) is False
            assert charged_battery.getCharge() == 100
        
        def test_already_empty(empty_battery):
            assert empty_battery.drain(10) is False
            assert empty_battery.getCharge() == 0
        
        def test_monitor_notification(charged_battery):
            monitor = Mock()
            charged_battery.external_monitor = monitor
            charged_battery.drain(30)
            monitor.notify_drain.assert_called_once_with(70)
    
    def describe_getters():
        def test_capacity(charged_battery):
            assert charged_battery.getCapacity() == 100

        def test_charge(partially_charged_battery):
            assert partially_charged_battery.getCharge() == 50