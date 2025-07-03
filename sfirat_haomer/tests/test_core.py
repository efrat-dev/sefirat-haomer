import pytest
import datetime
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List, Tuple

# Assuming the module structure - adjust imports as needed
from core import (
    OmerDay, OmerCalculator, SefiraInfo, OmerMonth, OmerTradition,
    get_omer_text_by_date, get_all_omer_days, get_omer_days_by_week,
    get_current_omer_status, get_omer_day_by_number, get_ana_bekoach_text,
    get_sefirot_attributes, find_special_omer_days, find_omer_day_by_gregorian_range,
    get_omer_summary_by_sefirah, export_omer_calendar, validate_omer_configuration,
    _get_omer_from_gregorian, _get_omer_from_hebrew, _create_omer_day
)


class TestOmerMonth:
    """Test OmerMonth enum"""
    
    def test_omer_month_values(self):
        assert OmerMonth.NISAN.value == "Nisan"
        assert OmerMonth.IYYAR.value == "Iyyar"
        assert OmerMonth.SIVAN.value == "Sivan"


class TestOmerTradition:
    """Test OmerTradition enum"""
    
    def test_omer_tradition_values(self):
        assert OmerTradition.SEFARDI.value == "sefardi"
        assert OmerTradition.ASHKENAZI.value == "ashkenazi"
        assert OmerTradition.CHASSIDIC.value == "chassidic"


class TestSefiraInfo:
    """Test SefiraInfo dataclass"""
    
    @pytest.fixture
    def sample_sefirah_info(self):
        return SefiraInfo(
            week_sefirah={"hebrew": "חסד", "english": "Chesed"},
            day_sefirah={"hebrew": "חסד", "english": "Chesed"},
            combination="חסד שבחסד",
            combination_transliteration="Chesed shebeChesed",
            combination_english="Kindness within Kindness"
        )
    
    def test_sefirah_info_creation(self, sample_sefirah_info):
        assert sample_sefirah_info.week_sefirah["hebrew"] == "חסד"
        assert sample_sefirah_info.combination == "חסד שבחסד"
        assert sample_sefirah_info.combination_english == "Kindness within Kindness"
    
    def test_format_sefirah_text_basic(self, sample_sefirah_info):
        result = sample_sefirah_info.format_sefirah_text()
        assert result == "חסד שבחסד"
    
    def test_format_sefirah_text_with_transliteration(self, sample_sefirah_info):
        result = sample_sefirah_info.format_sefirah_text(include_transliteration=True)
        assert result == "חסד שבחסד | Chesed shebeChesed"
    
    def test_format_sefirah_text_with_english(self, sample_sefirah_info):
        result = sample_sefirah_info.format_sefirah_text(include_english=True)
        assert result == "חסד שבחסד | Kindness within Kindness"
    
    def test_format_sefirah_text_full(self, sample_sefirah_info):
        result = sample_sefirah_info.format_sefirah_text(
            include_transliteration=True, 
            include_english=True
        )
        assert result == "חסד שבחסד | Chesed shebeChesed | Kindness within Kindness"


class TestOmerDay:
    """Test OmerDay dataclass"""
    
    @pytest.fixture
    def sample_omer_day(self):
        return OmerDay(
            day=1,
            text="היום יום אחד לעומר",
            transliteration="Hayom yom echad la'omer",
            english_translation="Today is one day of the Omer"
        )
    
    def test_omer_day_creation(self, sample_omer_day):
        assert sample_omer_day.day == 1
        assert sample_omer_day.text == "היום יום אחד לעומר"
        assert sample_omer_day.transliteration == "Hayom yom echad la'omer"
        assert sample_omer_day.english_translation == "Today is one day of the Omer"
    
    def test_omer_day_invalid_day(self):
        with pytest.raises(ValueError):
            OmerDay(day=0, text="test")
        
        with pytest.raises(ValueError):
            OmerDay(day=50, text="test")
    
    def test_week_property(self, sample_omer_day):
        assert sample_omer_day.week == 1
        
        day_8 = OmerDay(day=8, text="test")
        assert day_8.week == 2
        
        day_49 = OmerDay(day=49, text="test")
        assert day_49.week == 7
    
    def test_day_of_week_property(self, sample_omer_day):
        assert sample_omer_day.day_of_week == 1
        
        day_7 = OmerDay(day=7, text="test")
        assert day_7.day_of_week == 7
        
        day_8 = OmerDay(day=8, text="test")
        assert day_8.day_of_week == 1
    
    def test_is_complete_week_property(self, sample_omer_day):
        assert not sample_omer_day.is_complete_week
        
        day_7 = OmerDay(day=7, text="test")
        assert day_7.is_complete_week
        
        day_14 = OmerDay(day=14, text="test")
        assert day_14.is_complete_week
    
    def test_days_remaining_property(self, sample_omer_day):
        assert sample_omer_day.days_remaining == 48
        
        day_49 = OmerDay(day=49, text="test")
        assert day_49.days_remaining == 0
    
    def test_get_week_description_hebrew(self):
        # Test first week (no description)
        day_1 = OmerDay(day=1, text="test")
        assert day_1.get_week_description() == ""
        
        # Test second week
        day_8 = OmerDay(day=8, text="test")
        description = day_8.get_week_description()
        assert "שבוע אחד" in description
        assert "יום אחד" in description
        
        # Test complete week
        day_14 = OmerDay(day=14, text="test")
        description = day_14.get_week_description()
        assert "שבועות" in description
        assert "יום" not in description or "ימים" not in description  # No days, just weeks
    
    def test_get_week_description_english(self):
        day_8 = OmerDay(day=8, text="test")
        description = day_8.get_week_description(in_hebrew=False)
        assert "which are 1 week and 1 day" in description
        
        day_14 = OmerDay(day=14, text="test")
        description = day_14.get_week_description(in_hebrew=False)
        assert "which are 2 weeks" in description
    
    def test_to_dict(self, sample_omer_day):
        result = sample_omer_day.to_dict()
        assert isinstance(result, dict)
        assert result["day"] == 1
        assert result["text"] == "היום יום אחד לעומר"
        assert result["week"] == 1
        assert result["day_of_week"] == 1
        assert result["is_complete_week"] == False
        assert result["days_remaining"] == 48
    
    @patch('core.get_config')
    def test_format_output(self, mock_get_config, sample_omer_day):
        mock_config = MagicMock()
        mock_config.output_format = "full"
        mock_config.compact_output = False
        mock_get_config.return_value = mock_config
        
        result = sample_omer_day.format_output()
        assert isinstance(result, str)
        assert len(result) > 0


class TestOmerCalculator:
    """Test OmerCalculator class"""
    
    def test_is_omer_period_valid_dates(self):
        # Test valid Nisan dates
        assert OmerCalculator.is_omer_period(16, "Nisan") == True
        assert OmerCalculator.is_omer_period(30, "Nisan") == True
        
        # Test valid Iyyar dates
        assert OmerCalculator.is_omer_period(1, "Iyyar") == True
        assert OmerCalculator.is_omer_period(29, "Iyyar") == True
        
        # Test valid Sivan dates
        assert OmerCalculator.is_omer_period(1, "Sivan") == True
        assert OmerCalculator.is_omer_period(5, "Sivan") == True
    
    def test_is_omer_period_invalid_dates(self):
        # Test invalid Nisan dates
        assert OmerCalculator.is_omer_period(15, "Nisan") == False
        assert OmerCalculator.is_omer_period(31, "Nisan") == False
        
        # Test invalid Iyyar dates
        assert OmerCalculator.is_omer_period(30, "Iyyar") == False
        
        # Test invalid Sivan dates
        assert OmerCalculator.is_omer_period(6, "Sivan") == False
        
        # Test invalid months
        assert OmerCalculator.is_omer_period(1, "Tishrei") == False
    
    def test_calculate_omer_day_nisan(self):
        assert OmerCalculator.calculate_omer_day(16, "Nisan") == 1
        assert OmerCalculator.calculate_omer_day(30, "Nisan") == 15
    
    def test_calculate_omer_day_iyyar(self):
        assert OmerCalculator.calculate_omer_day(1, "Iyyar") == 16
        assert OmerCalculator.calculate_omer_day(29, "Iyyar") == 44
    
    def test_calculate_omer_day_sivan(self):
        assert OmerCalculator.calculate_omer_day(1, "Sivan") == 45
        assert OmerCalculator.calculate_omer_day(5, "Sivan") == 49
    
    def test_calculate_omer_day_invalid_month(self):
        with pytest.raises(ValueError):
            OmerCalculator.calculate_omer_day(1, "Tishrei")
    
    def test_get_hebrew_date_from_omer_day(self):
        # Test Nisan dates
        assert OmerCalculator.get_hebrew_date_from_omer_day(1) == (16, "Nisan")
        assert OmerCalculator.get_hebrew_date_from_omer_day(15) == (30, "Nisan")
        
        # Test Iyyar dates
        assert OmerCalculator.get_hebrew_date_from_omer_day(16) == (1, "Iyyar")
        assert OmerCalculator.get_hebrew_date_from_omer_day(44) == (29, "Iyyar")
        
        # Test Sivan dates
        assert OmerCalculator.get_hebrew_date_from_omer_day(45) == (1, "Sivan")
        assert OmerCalculator.get_hebrew_date_from_omer_day(49) == (5, "Sivan")
    
    def test_get_hebrew_date_from_omer_day_invalid(self):
        with pytest.raises(ValueError):
            OmerCalculator.get_hebrew_date_from_omer_day(0)
        
        with pytest.raises(ValueError):
            OmerCalculator.get_hebrew_date_from_omer_day(50)
    
    def test_get_weekday_info(self):
        test_date = datetime.date(2023, 4, 10)  # A Monday
        result = OmerCalculator.get_weekday_info(test_date)
        assert isinstance(result, dict)


class TestMainFunctions:
    """Test main module functions"""
    
    @patch('core.hebrew')
    @patch('core.get_config')
    def test_get_omer_text_by_date_none(self, mock_get_config, mock_hebrew):
        """Test getting today's Omer text"""
        mock_config = MagicMock()
        mock_get_config.return_value = mock_config
        
        with patch('core.datetime') as mock_datetime:
            mock_datetime.date.today.return_value = datetime.date(2023, 4, 10)
            mock_hebrew.from_gregorian.return_value = (5783, 1, 20)  # 20 Nisan
            
            result = get_omer_text_by_date()
            # Should return OmerDay or error string
            assert result is not None
    
    def test_get_omer_text_by_date_hebrew_date(self):
        """Test getting Omer text by Hebrew date"""
        result = get_omer_text_by_date((16, "Nisan"))
        assert isinstance(result, (OmerDay, str))
        
        if isinstance(result, OmerDay):
            assert result.day == 1
    
    @patch('core.hebrew')
    def test_get_omer_text_by_date_gregorian_date(self, mock_hebrew):
        """Test getting Omer text by Gregorian date"""
        mock_hebrew.from_gregorian.return_value = (5783, 1, 20)  # 20 Nisan
        
        test_date = datetime.date(2023, 4, 10)
        result = get_omer_text_by_date(test_date)
        assert isinstance(result, (OmerDay, str))
    
    def test_get_omer_text_by_date_invalid_input(self):
        """Test invalid input handling"""
        result = get_omer_text_by_date("invalid")
        assert isinstance(result, str)
        assert "error" in result.lower() or "invalid" in result.lower()
    
    @patch('core.hebrew')
    def test_get_all_omer_days(self, mock_hebrew):
        """Test getting all 49 Omer days"""
        mock_hebrew.from_gregorian.return_value = (5783, 1, 1)
        
        result = get_all_omer_days()
        assert isinstance(result, list)
        assert len(result) == 49
        
        # Check that all days are OmerDay instances
        for day in result:
            assert isinstance(day, OmerDay)
            assert 1 <= day.day <= 49
    
    @patch('core.get_all_omer_days')
    def test_get_omer_days_by_week(self, mock_get_all_days):
        """Test getting Omer days by week"""
        # Mock 49 days
        mock_days = [OmerDay(day=i, text=f"Day {i}") for i in range(1, 50)]
        mock_get_all_days.return_value = mock_days
        
        # Test week 1
        week_1 = get_omer_days_by_week(1)
        assert len(week_1) == 7
        assert all(1 <= day.day <= 7 for day in week_1)
        
        # Test week 7 (partial)
        week_7 = get_omer_days_by_week(7)
        assert len(week_7) == 7  # Days 43-49
        assert all(43 <= day.day <= 49 for day in week_7)
    
    def test_get_omer_days_by_week_invalid(self):
        """Test invalid week number"""
        with pytest.raises(ValueError):
            get_omer_days_by_week(0)
        
        with pytest.raises(ValueError):
            get_omer_days_by_week(8)
    
    @patch('core.get_omer_text_by_date')
    @patch('core.get_config')
    def test_get_current_omer_status_during_omer(self, mock_get_config, mock_get_omer):
        """Test getting current status during Omer period"""
        mock_config = MagicMock()
        mock_get_config.return_value = mock_config
        
        mock_omer_day = OmerDay(day=1, text="test")
        mock_get_omer.return_value = mock_omer_day
        
        result = get_current_omer_status()
        assert isinstance(result, dict)
        assert result["is_omer_period"] == True
        assert result["day"] == 1
        assert "text" in result
        assert "blessing" in result
    
    @patch('core.get_omer_text_by_date')
    @patch('core.get_config')
    def test_get_current_omer_status_outside_omer(self, mock_get_config, mock_get_omer):
        """Test getting current status outside Omer period"""
        mock_config = MagicMock()
        mock_get_config.return_value = mock_config
        
        mock_get_omer.return_value = "Not in Omer period"
        
        result = get_current_omer_status()
        assert isinstance(result, dict)
        assert result["is_omer_period"] == False
        assert "message" in result
    
    def test_get_omer_day_by_number_valid(self):
        """Test getting Omer day by valid number"""
        result = get_omer_day_by_number(1)
        assert isinstance(result, (OmerDay, str))
        
        if isinstance(result, OmerDay):
            assert result.day == 1
    
    def test_get_omer_day_by_number_invalid(self):
        """Test getting Omer day by invalid number"""
        result = get_omer_day_by_number(0)
        assert isinstance(result, str)
        assert "error" in result.lower() or "range" in result.lower()
        
        result = get_omer_day_by_number(50)
        assert isinstance(result, str)
        assert "error" in result.lower() or "range" in result.lower()
    
    def test_get_ana_bekoach_text(self):
        """Test getting Ana BeKoach text"""
        result = get_ana_bekoach_text()
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_get_sefirot_attributes(self):
        """Test getting Sefirot attributes"""
        result = get_sefirot_attributes()
        assert isinstance(result, dict)
        assert len(result) > 0
    
    @patch('core.get_omer_day_by_number')
    @patch('core.get_config')
    def test_find_special_omer_days(self, mock_get_config, mock_get_omer_day):
        """Test finding special Omer days"""
        mock_config = MagicMock()
        mock_get_config.return_value = mock_config
        
        mock_omer_day = OmerDay(day=33, text="test")
        mock_omer_day.is_special_day = True
        mock_get_omer_day.return_value = mock_omer_day
        
        result = find_special_omer_days()
        assert isinstance(result, list)
    
    @patch('core.get_omer_text_by_date')
    def test_find_omer_day_by_gregorian_range(self, mock_get_omer):
        """Test finding Omer days by Gregorian range"""
        mock_omer_day = OmerDay(day=1, text="test")
        mock_get_omer.return_value = mock_omer_day
        
        start_date = datetime.date(2023, 4, 10)
        end_date = datetime.date(2023, 4, 12)
        
        result = find_omer_day_by_gregorian_range(start_date, end_date)
        assert isinstance(result, list)
    
    @patch('core.get_omer_days_by_week')
    def test_get_omer_summary_by_sefirah(self, mock_get_week_days):
        """Test getting Omer summary by Sefirah"""
        mock_days = [OmerDay(day=i, text=f"Day {i}") for i in range(1, 8)]
        mock_get_week_days.return_value = mock_days
        
        result = get_omer_summary_by_sefirah(1)
        assert isinstance(result, dict)
        assert result["week"] == 1
        assert "sefirah" in result
        assert "days" in result
        assert result["total_days"] == 7
    
    def test_get_omer_summary_by_sefirah_invalid(self):
        """Test invalid Sefirah week"""
        with pytest.raises(ValueError):
            get_omer_summary_by_sefirah(0)
        
        with pytest.raises(ValueError):
            get_omer_summary_by_sefirah(8)
    
    @patch('core.get_all_omer_days')
    def test_export_omer_calendar_json(self, mock_get_all_days):
        """Test exporting Omer calendar as JSON"""
        mock_days = [OmerDay(day=i, text=f"Day {i}") for i in range(1, 50)]
        mock_get_all_days.return_value = mock_days
        
        result = export_omer_calendar(format_type="json")
        assert isinstance(result, dict)
        assert "total_days" in result
        assert "days" in result
        assert "special_days" in result
        assert "sefirot_attributes" in result
    
    @patch('core.get_all_omer_days')
    def test_export_omer_calendar_text(self, mock_get_all_days):
        """Test exporting Omer calendar as text"""
        mock_days = [OmerDay(day=i, text=f"Day {i}") for i in range(1, 50)]
        mock_get_all_days.return_value = mock_days
        
        result = export_omer_calendar(format_type="text")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_export_omer_calendar_invalid_format(self):
        """Test invalid export format"""
        with pytest.raises(ValueError):
            export_omer_calendar(format_type="invalid")
    
    @patch('core.validate_data_integrity')
    @patch('core.get_all_omer_days')
    def test_validate_omer_configuration(self, mock_get_all_days, mock_validate_data):
        """Test validating Omer configuration"""
        mock_validate_data.return_value = []
        mock_days = [OmerDay(day=i, text=f"Day {i}") for i in range(1, 50)]
        mock_get_all_days.return_value = mock_days
        
        result = validate_omer_configuration()
        assert isinstance(result, list)


class TestPrivateFunctions:
    """Test private/helper functions"""
    
    @patch('core.hebrew')
    def test_get_omer_from_gregorian_valid(self, mock_hebrew):
        """Test getting Omer from valid Gregorian date"""
        mock_hebrew.from_gregorian.return_value = (5783, 1, 20)  # 20 Nisan
        
        test_date = datetime.date(2023, 4, 10)
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _get_omer_from_gregorian(test_date, config, tradition)
        assert isinstance(result, (OmerDay, str))
    
    @patch('core.hebrew')
    def test_get_omer_from_gregorian_invalid(self, mock_hebrew):
        """Test getting Omer from invalid Gregorian date"""
        mock_hebrew.from_gregorian.side_effect = ValueError("Invalid date")
        
        test_date = datetime.date(2023, 4, 10)
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _get_omer_from_gregorian(test_date, config, tradition)
        assert isinstance(result, str)
        assert "error" in result.lower()
    
    def test_get_omer_from_hebrew_valid(self):
        """Test getting Omer from valid Hebrew date"""
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _get_omer_from_hebrew(16, "Nisan", config, tradition)
        assert isinstance(result, (OmerDay, str))
    
    def test_get_omer_from_hebrew_invalid_month(self):
        """Test getting Omer from invalid Hebrew month"""
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _get_omer_from_hebrew(1, "Tishrei", config, tradition)
        assert isinstance(result, str)
        assert "Invalid Hebrew month" in result
    
    def test_get_omer_from_hebrew_invalid_day(self):
        """Test getting Omer from invalid Hebrew day"""
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _get_omer_from_hebrew(32, "Nisan", config, tradition)
        assert isinstance(result, str)
        assert "Invalid day" in result
    
    def test_create_omer_day_valid(self):
        """Test creating valid Omer day"""
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _create_omer_day(16, "Nisan", config, tradition)
        assert isinstance(result, (OmerDay, str))
    
    def test_create_omer_day_invalid_period(self):
        """Test creating Omer day outside period"""
        config = MagicMock()
        tradition = OmerTradition.ASHKENAZI
        
        result = _create_omer_day(15, "Nisan", config, tradition)
        assert isinstance(result, str)
        assert "not within the Sefirat HaOmer period" in result


class TestIntegration:
    """Integration tests"""
    
    def test_full_omer_cycle(self):
        """Test complete Omer counting cycle"""
        # Test that we can get all 49 days
        for day_num in range(1, 50):
            result = get_omer_day_by_number(day_num)
            assert isinstance(result, (OmerDay, str))
            
            if isinstance(result, OmerDay):
                assert result.day == day_num
                assert 1 <= result.week <= 7
                assert 1 <= result.day_of_week <= 7
    
    def test_hebrew_date_consistency(self):
        """Test consistency between Hebrew dates and Omer days"""
        # Test known conversions
        test_cases = [
            (16, "Nisan", 1),
            (30, "Nisan", 15),
            (1, "Iyyar", 16),
            (29, "Iyyar", 44),
            (1, "Sivan", 45),
            (5, "Sivan", 49)
        ]
        
        for day, month, expected_omer in test_cases:
            if OmerCalculator.is_omer_period(day, month):
                calculated_omer = OmerCalculator.calculate_omer_day(day, month)
                assert calculated_omer == expected_omer
                
                # Test reverse conversion
                hebrew_date = OmerCalculator.get_hebrew_date_from_omer_day(expected_omer)
                assert hebrew_date == (day, month)


# Fixtures for mock data
@pytest.fixture
def mock_omer_texts():
    """Mock Omer texts for testing"""
    return {i: f"Day {i} text" for i in range(1, 50)}


@pytest.fixture
def mock_omer_transliterations():
    """Mock Omer transliterations for testing"""
    return {i: f"Day {i} transliteration" for i in range(1, 50)}


@pytest.fixture
def mock_omer_english_translations():
    """Mock Omer English translations for testing"""
    return {i: f"Day {i} English" for i in range(1, 50)}


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])