MOCK_ANA_BEKOACH = {
    'hebrew': [
        'אנא בכח גדולת ימינך תתיר צרורה',
        'קבל רנת עמך שגבנו טהרנו נורא'
    ],
    'transliteration': [
        'Ana b\'koach g\'dulat y\'mincha tatir tz\'rurah',
        'Kabel rinat amcha sagvenu taharenu nora'
    ],
    'english': [
        'Please, with the strength of Your right hand, release the bound',
        'Accept the prayer of Your people; strengthen us, purify us, Awesome One'
    ]
}


class TestCLIFormatting:
    """Test formatting functions"""
    
    def test_format_omer_day_detailed(self):
        """Test detailed formatting of Omer day"""
        formatted = format_omer_day(MOCK_OMER_DAY)
        
        assert "Day 15 of the Omer" in formatted
        assert "Week 3, Day 1" in formatted
        assert "היום חמישה עשר יום" in formatted
        assert "חסד שבתפארת" in formatted
        assert "18 Iyyar" in formatted
        assert "2024-05-15" in formatted

    def test_format_omer_day_compact(self):
        """Test compact formatting of Omer day"""
        formatted = format_omer_day(MOCK_OMER_DAY, compact=True)
        
        assert "Day 15:" in formatted
        assert "היום חמישה עשר יום" in formatted
        assert len(formatted.split('\n')) == 1  # Should be single line

    def test_format_omer_day_missing_field(self):
        """Test formatting with missing required field"""
        incomplete_day = {'week': 3}  # Missing 'day' field
        
        with pytest.raises(OmerCLIOutputError) as exc_info:
            format_omer_day(incomplete_day)
        
        assert "Missing required field" in str(exc_info.value)

    def test_format_omer_day_special_day(self):
        """Test formatting of special day"""
        formatted = format_omer_day(MOCK_SPECIAL_DAY)
        
        assert "Day 33 of the Omer" in formatted
        assert "Special Day:" in formatted
        assert "לג בעומר" in formatted or "Lag BaOmer" in formatted

    def test_display_blessing_basic(self, capsys):
        """Test basic blessing display"""
        blessing_data = {
            'hebrew': 'ברוך אתה השם אלוקינו מלך העולם',
            'transliteration': 'Baruch atah Hashem Elokeinu melech ha\'olam',
            'english': 'Blessed are You, Hashem our God, King of the universe'
        }
        
        display_blessing(blessing_data)
        captured = capsys.readouterr()
        
        assert "Blessing for Counting the Omer" in captured.out
        assert "ברוך אתה השם אלוקינו" in captured.out
        assert "Baruch atah Hashem" in captured.out

    def test_display_blessing_with_intro(self, capsys):
        """Test blessing display with introduction"""
        blessing_data = {
            'intro': 'הנני מוכן ומזומן',
            'intro_transliteration': 'Hineni muchan u\'m\'zuman',
            'intro_english': 'I am ready and prepared',
            'hebrew': 'ברוך אתה השם אלוקינו מלך העולם',
            'transliteration': 'Baruch atah Hashem Elokeinu melech ha\'olam',
            'english': 'Blessed are You, Hashem our God, King of the universe'
        }
        
        display_blessing(blessing_data)
        captured = capsys.readouterr()
        
        assert "הנני מוכן ומזומן" in captured.out
        assert "Hineni muchan" in captured.out


class TestCLICommands:
    """Test CLI command functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()

    @patch('cli.get_current_omer_status')
    def test_today_command_basic(self, mock_status):
        """Test basic today command"""
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        result = self.runner.invoke(cli, ['today'])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output
        mock_status.assert_called_once()

    @patch('cli.get_current_omer_status')
    def test_today_command_with_blessing(self, mock_status):
        """Test today command with blessing"""
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        result = self.runner.invoke(cli, ['today', '--blessing'])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output
        assert "ברוך אתה השם אלוקינו" in result.output

    @patch('cli.get_current_omer_status')
    def test_today_command_with_prayer(self, mock_status):
        """Test today command with prayer"""
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        result = self.runner.invoke(cli, ['today', '--prayer'])
        
        assert result.exit_code == 0
        assert "Prayer after counting" in result.output
        assert "הרחמן הוא יחזיר" in result.output

    @patch('cli.get_current_omer_status')
    def test_today_command_with_sefirah(self, mock_status):
        """Test today command with sefirah info"""
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        result = self.runner.invoke(cli, ['today', '--sefirah'])
        
        assert result.exit_code == 0
        assert "Detailed Sefirah Information" in result.output
        assert "חסד שבתפארת" in result.output

    @patch('cli.get_current_omer_status')
    def test_today_command_not_omer_period(self, mock_status):
        """Test today command when not in Omer period"""
        mock_status.return_value = {
            'is_omer_period': False,
            'message': 'Not in Omer period'
        }
        
        result = self.runner.invoke(cli, ['today'])
        
        assert result.exit_code == 0
        assert "We are not currently in the Sefirat HaOmer period" in result.output

    @patch('cli.get_omer_day_by_number')
    def test_day_command_valid(self, mock_get_day):
        """Test day command with valid day number"""
        mock_omer_day = MagicMock()
        mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
        mock_get_day.return_value = mock_omer_day
        
        result = self.runner.invoke(cli, ['day', '15'])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output
        mock_get_day.assert_called_once_with(15, tradition=unittest.mock.ANY)

    def test_day_command_invalid_number(self):
        """Test day command with invalid day number"""
        result = self.runner.invoke(cli, ['day', '0'])
        
        assert result.exit_code != 0
        assert "Day number must be between 1 and 49" in result.output

    def test_day_command_too_high(self):
        """Test day command with day number too high"""
        result = self.runner.invoke(cli, ['day', '50'])
        
        assert result.exit_code != 0
        assert "Day number must be between 1 and 49" in result.output

    @patch('cli.get_omer_day_by_number')
    def test_day_command_with_blessing(self, mock_get_day):
        """Test day command with blessing option"""
        mock_omer_day = MagicMock()
        mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
        mock_omer_day.get_blessing_text.return_value = {
            'hebrew': 'ברוך אתה השם אלוקינו מלך העולם',
            'transliteration': 'Baruch atah Hashem',
            'english': 'Blessed are You, Hashem'
        }
        mock_get_day.return_value = mock_omer_day
        
        result = self.runner.invoke(cli, ['day', '15', '--blessing'])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output
        assert "ברוך אתה השם אלוקינו" in result.output

    @patch('cli.get_omer_days_by_week')
    @patch('cli.get_omer_summary_by_sefirah')
    def test_week_command_valid(self, mock_summary, mock_get_week):
        """Test week command with valid week number"""
        mock_days = [MagicMock() for _ in range(7)]
        for i, day in enumerate(mock_days):
            day_data = MOCK_OMER_DAY.copy()
            day_data['day'] = i + 1
            day.to_dict.return_value = day_data
        
        mock_get_week.return_value = mock_days
        mock_summary.return_value = {
            'sefirah': {
                'hebrew': 'חסד',
                'transliteration': 'Chesed',
                'english': 'Loving-kindness',
                'attribute': 'Love and kindness'
            }
        }
        
        result = self.runner.invoke(cli, ['week', '1'])
        
        assert result.exit_code == 0
        assert "Week 1 of the Omer" in result.output
        assert "חסד" in result.output
        mock_get_week.assert_called_once_with(1, tradition=unittest.mock.ANY)

    def test_week_command_invalid_number(self):
        """Test week command with invalid week number"""
        result = self.runner.invoke(cli, ['week', '0'])
        
        assert result.exit_code != 0
        assert "Week number must be between 1 and 7" in result.output

    def test_week_command_too_high(self):
        """Test week command with week number too high"""
        result = self.runner.invoke(cli, ['week', '8'])
        
        assert result.exit_code != 0
        assert "Week number must be between 1 and 7" in result.output

    @patch('cli.get_omer_days_by_week')
    @patch('cli.get_omer_summary_by_sefirah')
    def test_week_command_compact(self, mock_summary, mock_get_week):
        """Test week command with compact output"""
        mock_days = [MagicMock() for _ in range(7)]
        for i, day in enumerate(mock_days):
            day_data = MOCK_OMER_DAY.copy()
            day_data['day'] = i + 1
            day.to_dict.return_value = day_data
        
        mock_get_week.return_value = mock_days
        mock_summary.return_value = {
            'sefirah': {
                'hebrew': 'חסד',
                'transliteration': 'Chesed',
                'english': 'Loving-kindness',
                'attribute': 'Love and kindness'
            }
        }
        
        result = self.runner.invoke(cli, ['week', '1', '--compact'])
        
        assert result.exit_code == 0
        # Should not have detailed week summary in compact mode
        assert "Week 1 of the Omer" not in result.output

    @patch('cli.find_omer_day_by_gregorian_range')
    def test_range_command_valid(self, mock_range):
        """Test range command with valid dates"""
        mock_days = [MagicMock() for _ in range(3)]
        for i, day in enumerate(mock_days):
            day_data = MOCK_OMER_DAY.copy()
            day_data['day'] = i + 1
            day.to_dict.return_value = day_data
        
        mock_range.return_value = mock_days
        
        result = self.runner.invoke(cli, [
            'range', 
            '--start-date', '2024-04-15',
            '--end-date', '2024-04-17'
        ])
        
        assert result.exit_code == 0
        assert "Found 3 Omer days" in result.output

    def test_range_command_missing_dates(self):
        """Test range command with missing dates"""
        result = self.runner.invoke(cli, [
            'range', 
            '--start-date', '2024-04-15'
        ])
        
        assert result.exit_code != 0
        assert "Both start-date and end-date are required" in result.output

    def test_range_command_invalid_date_order(self):
        """Test range command with end date before start date"""
        result = self.runner.invoke(cli, [
            'range',
            '--start-date', '2024-04-17',
            '--end-date', '2024-04-15'
        ])
        
        assert result.exit_code != 0
        assert "Start date must be before end date" in result.output

    @patch('cli.find_omer_day_by_gregorian_range')
    def test_range_command_no_results(self, mock_range):
        """Test range command with no Omer days found"""
        mock_range.return_value = []
        
        result = self.runner.invoke(cli, [
            'range',
            '--start-date', '2024-01-01',
            '--end-date', '2024-01-31'
        ])
        
        assert result.exit_code == 0
        assert "No Omer days found" in result.output

    @patch('cli.find_special_omer_days')
    def test_special_command(self, mock_special):
        """Test special command"""
        mock_special_day = MagicMock()
        mock_special_day.to_dict.return_value = MOCK_SPECIAL_DAY
        mock_special.return_value = [mock_special_day]
        
        result = self.runner.invoke(cli, ['special'])
        
        assert result.exit_code == 0
        assert "Special Days during Sefirat HaOmer" in result.output
        assert "Day 33:" in result.output

    @patch('cli.find_special_omer_days')
    def test_special_command_no_results(self, mock_special):
        """Test special command with no special days"""
        mock_special.return_value = []
        
        result = self.runner.invoke(cli, ['special'])
        
        assert result.exit_code == 0
        assert "No special days found" in result.output

    @patch('cli.export_omer_calendar')
    def test_export_command_json(self, mock_export):
        """Test export command with JSON format"""
        mock_export.return_value = {'test': 'data'}
        
        result = self.runner.invoke(cli, ['export', '--format', 'json'])
        
        assert result.exit_code == 0
        assert '{"test": "data"}' in result.output

    @patch('cli.export_omer_calendar')
    def test_export_command_text(self, mock_export):
        """Test export command with text format"""
        mock_export.return_value = "Test calendar data"
        
        result = self.runner.invoke(cli, ['export', '--format', 'text'])
        
        assert result.exit_code == 0
        assert "Test calendar data" in result.output

    @patch('cli.export_omer_calendar')
    def test_export_command_to_file(self, mock_export):
        """Test export command to file"""
        mock_export.return_value = {'test': 'data'}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            result = self.runner.invoke(cli, [
                'export', '--format', 'json', '--output', temp_file
            ])
            
            assert result.exit_code == 0
            assert f"Calendar exported to {temp_file}" in result.output
            
            with open(temp_file, 'r') as f:
                data = json.load(f)
                assert data == {'test': 'data'}
        finally:
            os.unlink(temp_file)

    def test_export_command_invalid_format(self):
        """Test export command with invalid format"""
        result = self.runner.invoke(cli, ['export', '--format', 'invalid'])
        
        assert result.exit_code != 0

    @patch('cli.get_sefirot_attributes')
    def test_sefirot_command(self, mock_sefirot):
        """Test sefirot command"""
        mock_sefirot.return_value = MOCK_SEFIROT
        
        result = self.runner.invoke(cli, ['sefirot'])
        
        assert result.exit_code == 0
        assert "The Ten Sefirot" in result.output
        assert "חסד" in result.output
        assert "Chesed" in result.output

    @patch('cli.get_ana_bekoach_text')
    def test_ana_bekoach_command(self, mock_ana):
        """Test ana-bekoach command"""
        mock_ana.return_value = MOCK_ANA_BEKOACH
        
        result = self.runner.invoke(cli, ['ana-bekoach'])
        
        assert result.exit_code == 0
        assert "Ana BeKoach Prayer" in result.output
        assert "אנא בכח גדולת ימינך" in result.output

    @patch('cli.get_omer_text_by_date')
    def test_hebrew_date_command_valid(self, mock_get_date):
        """Test hebrew-date command with valid date"""
        mock_omer_day = MagicMock()
        mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
        mock_get_date.return_value = mock_omer_day
        
        result = self.runner.invoke(cli, ['hebrew-date', '18', 'Iyyar'])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output
        mock_get_date.assert_called_once_with(
            date=(18, 'Iyyar'), 
            tradition=unittest.mock.ANY
        )

    def test_hebrew_date_command_invalid_day(self):
        """Test hebrew-date command with invalid day"""
        result = self.runner.invoke(cli, ['hebrew-date', '0', 'Iyyar'])
        
        assert result.exit_code != 0
        assert "Hebrew day must be between 1-30" in result.output

    def test_hebrew_date_command_invalid_month(self):
        """Test hebrew-date command with empty month"""
        result = self.runner.invoke(cli, ['hebrew-date', '15', ''])
        
        assert result.exit_code != 0
        assert "Hebrew month must be a non-empty string" in result.output

    @patch('cli.get_omer_text_by_date')
    def test_gregorian_date_command_valid(self, mock_get_date):
        """Test gregorian-date command with valid date"""
        mock_omer_day = MagicMock()
        mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
        mock_get_date.return_value = mock_omer_day
        
        result = self.runner.invoke(cli, ['gregorian-date', '2024-05-15'])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output

    @patch('cli.validate_omer_configuration')
    def test_validate_command_success(self, mock_validate):
        """Test validate command with successful validation"""
        mock_validate.return_value = []
        
        result = self.runner.invoke(cli, ['validate'])
        
        assert result.exit_code == 0
        assert "All validations passed successfully" in result.output

    @patch('cli.validate_omer_configuration')
    def test_validate_command_errors(self, mock_validate):
        """Test validate command with validation errors"""
        mock_validate.return_value = ['Error 1', 'Error 2']
        
        result = self.runner.invoke(cli, ['validate'])
        
        assert result.exit_code != 0
        assert "Validation errors found" in result.output
        assert "Error 1" in result.output
        assert "Error 2" in result.output

    @patch('cli.get_current_omer_status')
    def test_status_command_in_period(self, mock_status):
        """Test status command during Omer period"""
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        result = self.runner.invoke(cli, ['status'])
        
        assert result.exit_code == 0
        assert "Current Omer Status" in result.output
        assert "Days remaining: 34" in result.output

    @patch('cli.get_current_omer_status')
    def test_status_command_not_in_period(self, mock_status):
        """Test status command outside Omer period"""
        mock_status.return_value = {
            'is_omer_period': False,
            'message': 'Not in Omer period'
        }
        
        result = self.runner.invoke(cli, ['status'])
        
        assert result.exit_code == 0
        assert "Not currently in Omer period" in result.output

    def test_process_file_command_valid(self):
        """Test process-file command with valid input"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test Omer data")
            input_file = f.name
        
        try:
            result = self.runner.invoke(cli, ['process-file', input_file])
            
            assert result.exit_code == 0
            assert "Processed Omer data" in result.output
            assert "Test Omer data" in result.output
        finally:
            os.unlink(input_file)

    def test_process_file_command_with_output(self):
        """Test process-file command with output file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test Omer data")
            input_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            output_file = f.name
        
        try:
            result = self.runner.invoke(cli, [
                'process-file', input_file, '--output', output_file
            ])
            
            assert result.exit_code == 0
            assert f"Processed data saved to {output_file}" in result.output
            
            with open(output_file, 'r') as f:
                content = f.read()
                assert "Processed Omer data" in content
                assert "Test Omer data" in content
        finally:
            os.unlink(input_file)
            os.unlink(output_file)

    def test_process_file_command_nonexistent_file(self):
        """Test process-file command with non-existent file"""
        result = self.runner.invoke(cli, ['process-file', 'nonexistent.txt'])
        
        assert result.exit_code != 0


class TestCLIOptions:
    """Test CLI global options"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()

    def test_tradition_option_ashkenazi(self):
        """Test tradition option with Ashkenazi"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--tradition', 'ashkenazi', 'today'])
            
            assert result.exit_code == 0

    def test_tradition_option_sefardi(self):
        """Test tradition option with Sefardi"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--tradition', 'sefardi', 'today'])
            
            assert result.exit_code == 0

    def test_tradition_option_chassidic(self):
        """Test tradition option with Chassidic"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--tradition', 'chassidic', 'today'])
            
            assert result.exit_code == 0

    def test_tradition_option_invalid(self):
        """Test tradition option with invalid value"""
        result = self.runner.invoke(cli, ['--tradition', 'invalid', 'today'])
        
        assert result.exit_code != 0

    def test_format_option_detailed(self):
        """Test format option with detailed"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--format', 'detailed', 'today'])
            
            assert result.exit_code == 0

    def test_format_option_simple(self):
        """Test format option with simple"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--format', 'simple', 'today'])
            
            assert result.exit_code == 0

    def test_format_option_compact(self):
        """Test format option with compact"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--format', 'compact', 'today'])
            
            assert result.exit_code == 0

    def test_dates_option_hebrew(self):
        """Test dates option with Hebrew"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--dates', 'hebrew', 'today'])
            
            assert result.exit_code == 0

    def test_dates_option_gregorian(self):
        """Test dates option with Gregorian"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--dates', 'gregorian', 'today'])
            
            assert result.exit_code == 0

    def test_dates_option_both(self):
        """Test dates option with both"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--dates', 'both', 'today'])
            
            assert result.exit_code == 0

    def test_dates_option_iso(self):
        """Test dates option with ISO"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = {
                'is_omer_period': False,
                'message': 'Not in period'
            }
            
            result = self.runner.invoke(cli, ['--dates', 'iso', 'today'])
            
            assert result.exit_code == 0


class TestCLIErrorHandling:
    """Test CLI error handling"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()
def test_cli_error_handling_decorator(self):
        """Test that CLI error handling decorator works"""
        from exceptions import handle_cli_errors
        
        @handle_cli_errors
        def test_function():
            raise OmerCLIError("Test error")
        
        with pytest.raises(click.ClickException):
            test_function()

def test_cli_argument_error_handling(self):
        """Test CLI argument error handling"""
        result = self.runner.invoke(cli, ['day', 'invalid'])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower()

def test_cli_file_error_handling(self):
        """Test CLI file error handling"""
        result = self.runner.invoke(cli, ['process-file', 'nonexistent.txt'])
        
        assert result.exit_code != 0

def test_cli_output_error_handling(self):
        """Test CLI output error handling"""
        with patch('cli.format_omer_day') as mock_format:
            mock_format.side_effect = OmerCLIOutputError("Format error")
            
            result = self.runner.invoke(cli, ['day', '15'])
            
            assert result.exit_code != 0


class TestCLIIntegration:
    """Integration tests for CLI components"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()

    @patch('cli.get_current_omer_status')
    @patch('cli.get_omer_day_by_number')
    def test_full_workflow_today_with_options(self, mock_get_day, mock_status):
        """Test complete workflow with all options"""
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        result = self.runner.invoke(cli, [
            '--tradition', 'sefardi',
            '--format', 'detailed',
            '--dates', 'both',
            'today',
            '--blessing',
            '--prayer',
            '--sefirah'
        ])
        
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output
        assert "ברוך אתה השם אלוקינו" in result.output
        assert "הרחמן הוא יחזיר" in result.output
        assert "חסד שבתפארת" in result.output

    @patch('cli.get_omer_days_by_week')
    @patch('cli.get_omer_summary_by_sefirah')
    @patch('cli.get_omer_day_by_number')
    def test_full_workflow_week_to_day(self, mock_get_day, mock_summary, mock_get_week):
        """Test workflow from week to specific day"""
        # Setup mocks
        mock_days = [MagicMock() for _ in range(7)]
        for i, day in enumerate(mock_days):
            day_data = MOCK_OMER_DAY.copy()
            day_data['day'] = i + 1
            day.to_dict.return_value = day_data
        
        mock_get_week.return_value = mock_days
        mock_summary.return_value = {
            'sefirah': {
                'hebrew': 'חסד',
                'transliteration': 'Chesed',
                'english': 'Loving-kindness',
                'attribute': 'Love and kindness'
            }
        }
        
        mock_omer_day = MagicMock()
        mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
        mock_get_day.return_value = mock_omer_day
        
        # Test week command
        result = self.runner.invoke(cli, ['week', '1'])
        assert result.exit_code == 0
        assert "Week 1 of the Omer" in result.output
        
        # Test specific day from that week
        result = self.runner.invoke(cli, ['day', '1'])
        assert result.exit_code == 0
        assert "Day 15 of the Omer" in result.output

    @patch('cli.find_omer_day_by_gregorian_range')
    @patch('cli.find_special_omer_days')
    def test_full_workflow_range_to_special(self, mock_special, mock_range):
        """Test workflow from range to special days"""
        # Setup range mock
        mock_days = [MagicMock() for _ in range(5)]
        for i, day in enumerate(mock_days):
            day_data = MOCK_OMER_DAY.copy()
            day_data['day'] = i + 1
            day.to_dict.return_value = day_data
        
        mock_range.return_value = mock_days
        
        # Setup special days mock
        mock_special_day = MagicMock()
        mock_special_day.to_dict.return_value = MOCK_SPECIAL_DAY
        mock_special.return_value = [mock_special_day]
        
        # Test range command
        result = self.runner.invoke(cli, [
            'range',
            '--start-date', '2024-04-15',
            '--end-date', '2024-04-20'
        ])
        assert result.exit_code == 0
        assert "Found 5 Omer days" in result.output
        
        # Test special days command
        result = self.runner.invoke(cli, ['special'])
        assert result.exit_code == 0
        assert "Day 33:" in result.output


class TestCLIPerformance:
    """Performance tests for CLI operations"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()

    @patch('cli.get_current_omer_status')
    def test_today_command_performance(self, mock_status):
        """Test performance of today command"""
        import time
        
        mock_status.return_value = MOCK_CURRENT_STATUS
        
        start_time = time.time()
        result = self.runner.invoke(cli, ['today'])
        end_time = time.time()
        
        assert result.exit_code == 0
        # Should complete in under 1 second
        assert (end_time - start_time) < 1.0

    @patch('cli.get_omer_days_by_week')
    @patch('cli.get_omer_summary_by_sefirah')
    def test_week_command_performance(self, mock_summary, mock_get_week):
        """Test performance of week command"""
        import time
        
        # Setup large dataset
        mock_days = [MagicMock() for _ in range(7)]
        for i, day in enumerate(mock_days):
            day_data = MOCK_OMER_DAY.copy()
            day_data['day'] = i + 1
            day.to_dict.return_value = day_data
        
        mock_get_week.return_value = mock_days
        mock_summary.return_value = {
            'sefirah': {
                'hebrew': 'חסד',
                'transliteration': 'Chesed',
                'english': 'Loving-kindness',
                'attribute': 'Love and kindness'
            }
        }
        
        start_time = time.time()
        result = self.runner.invoke(cli, ['week', '1'])
        end_time = time.time()
        
        assert result.exit_code == 0
        # Should complete in under 2 seconds
        assert (end_time - start_time) < 2.0

    @patch('cli.export_omer_calendar')
    def test_export_command_performance(self, mock_export):
        """Test performance of export command"""
        import time
        
        # Create large mock data
        large_data = {f'day_{i}': f'data_{i}' for i in range(49)}
        mock_export.return_value = large_data
        
        start_time = time.time()
        result = self.runner.invoke(cli, ['export', '--format', 'json'])
        end_time = time.time()
        
        assert result.exit_code == 0
        # Should complete in under 3 seconds
        assert (end_time - start_time) < 3.0


class TestCLIDataIntegrity:
    """Data integrity tests for CLI"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()

    @patch('cli.get_omer_day_by_number')
    def test_data_consistency_across_days(self, mock_get_day):
        """Test data consistency across different days"""
        # Test multiple days to ensure consistency
        for day_num in [1, 15, 33, 49]:
            mock_day_data = MOCK_OMER_DAY.copy()
            mock_day_data['day'] = day_num
            
            mock_omer_day = MagicMock()
            mock_omer_day.to_dict.return_value = mock_day_data
            mock_get_day.return_value = mock_omer_day
            
            result = self.runner.invoke(cli, ['day', str(day_num)])
            
            assert result.exit_code == 0
            assert f"Day {day_num} of the Omer" in result.output

    @patch('cli.get_omer_days_by_week')
    @patch('cli.get_omer_summary_by_sefirah')
    def test_data_consistency_across_weeks(self, mock_summary, mock_get_week):
        """Test data consistency across different weeks"""
        # Test multiple weeks
        for week_num in [1, 3, 7]:
            mock_days = [MagicMock() for _ in range(7)]
            for i, day in enumerate(mock_days):
                day_data = MOCK_OMER_DAY.copy()
                day_data['day'] = (week_num - 1) * 7 + i + 1
                day_data['week'] = week_num
                day.to_dict.return_value = day_data
            
            mock_get_week.return_value = mock_days
            mock_summary.return_value = {
                'sefirah': {
                    'hebrew': 'חסד',
                    'transliteration': 'Chesed',
                    'english': 'Loving-kindness',
                    'attribute': 'Love and kindness'
                }
            }
            
            result = self.runner.invoke(cli, ['week', str(week_num)])
            
            assert result.exit_code == 0
            assert f"Week {week_num} of the Omer" in result.output

    @patch('cli.get_sefirot_attributes')
    def test_sefirot_data_integrity(self, mock_sefirot):
        """Test Sefirot data integrity"""
        # Ensure all required fields are present
        complete_sefirot = {}
        for i in range(1, 8):  # 7 weeks of Omer
            complete_sefirot[i] = {
                'hebrew': f'ספירה {i}',
                'transliteration': f'Sefirah {i}',
                'english': f'Sefirah {i}',
                'attribute': f'Attribute {i}'
            }
        
        mock_sefirot.return_value = complete_sefirot
        
        result = self.runner.invoke(cli, ['sefirot'])
        
        assert result.exit_code == 0
        assert "The Ten Sefirot" in result.output
        for i in range(1, 8):
            assert f"ספירה {i}" in result.output

    @patch('cli.get_ana_bekoach_text')
    def test_ana_bekoach_data_integrity(self, mock_ana):
        """Test Ana BeKoach data integrity"""
        complete_ana_bekoach = {
            'hebrew': ['Line 1', 'Line 2'],
            'transliteration': ['Trans 1', 'Trans 2'],
            'english': ['Eng 1', 'Eng 2']
        }
        
        mock_ana.return_value = complete_ana_bekoach
        
        result = self.runner.invoke(cli, ['ana-bekoach'])
        
        assert result.exit_code == 0
        assert "Ana BeKoach Prayer" in result.output
        assert "Line 1" in result.output
        assert "Trans 1" in result.output
        assert "Eng 1" in result.output


class TestCLIEdgeCases:
    """Edge case tests for CLI"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()

    def test_boundary_day_numbers(self):
        """Test boundary conditions for day numbers"""
        # Test day 1 (first day)
        with patch('cli.get_omer_day_by_number') as mock_get_day:
            mock_omer_day = MagicMock()
            mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
            mock_get_day.return_value = mock_omer_day
            
            result = self.runner.invoke(cli, ['day', '1'])
            assert result.exit_code == 0
        
        # Test day 49 (last day)
        with patch('cli.get_omer_day_by_number') as mock_get_day:
            mock_omer_day = MagicMock()
            mock_omer_day.to_dict.return_value = MOCK_OMER_DAY
            mock_get_day.return_value = mock_omer_day
            
            result = self.runner.invoke(cli, ['day', '49'])
            assert result.exit_code == 0

    def test_boundary_week_numbers(self):
        """Test boundary conditions for week numbers"""
        # Test week 1 (first week)
        with patch('cli.get_omer_days_by_week') as mock_get_week:
            with patch('cli.get_omer_summary_by_sefirah') as mock_summary:
                mock_days = [MagicMock() for _ in range(7)]
                for i, day in enumerate(mock_days):
                    day_data = MOCK_OMER_DAY.copy()
                    day_data['day'] = i + 1
                    day.to_dict.return_value = day_data
                
                mock_get_week.return_value = mock_days
                mock_summary.return_value = {
                    'sefirah': {
                        'hebrew': 'חסד',
                        'transliteration': 'Chesed',
                        'english': 'Loving-kindness',
                        'attribute': 'Love and kindness'
                    }
                }
                
                result = self.runner.invoke(cli, ['week', '1'])
                assert result.exit_code == 0
        
        # Test week 7 (last week)
        with patch('cli.get_omer_days_by_week') as mock_get_week:
            with patch('cli.get_omer_summary_by_sefirah') as mock_summary:
                mock_days = [MagicMock() for _ in range(7)]
                for i, day in enumerate(mock_days):
                    day_data = MOCK_OMER_DAY.copy()
                    day_data['day'] = 43 + i
                    day_data['week'] = 7
                    day.to_dict.return_value = day_data
                
                mock_get_week.return_value = mock_days
                mock_summary.return_value = {
                    'sefirah': {
                        'hebrew': 'מלכות',
                        'transliteration': 'Malchut',
                        'english': 'Kingdom',
                        'attribute': 'Kingdom and sovereignty'
                    }
                }
                
                result = self.runner.invoke(cli, ['week', '7'])
                assert result.exit_code == 0

    def test_empty_data_handling(self):
        """Test handling of empty or missing data"""
        with patch('cli.find_special_omer_days') as mock_special:
            mock_special.return_value = []
            
            result = self.runner.invoke(cli, ['special'])
            assert result.exit_code == 0
            assert "No special days found" in result.output

    def test_malformed_date_handling(self):
        """Test handling of malformed dates"""
        result = self.runner.invoke(cli, ['gregorian-date', 'invalid-date'])
        assert result.exit_code != 0

    def test_unicode_handling(self):
        """Test proper Unicode handling"""
        with patch('cli.get_current_omer_status') as mock_status:
            mock_status.return_value = MOCK_CURRENT_STATUS
            
            result = self.runner.invoke(cli, ['today'])
            assert result.exit_code == 0
            # Should handle Hebrew text properly
            assert "היום חמישה עשר יום" in result.output

    def test_large_date_ranges(self):
        """Test handling of large date ranges"""
        with patch('cli.find_omer_day_by_gregorian_range') as mock_range:
            # Mock large result set
            large_result = [MagicMock() for _ in range(49)]
            for i, day in enumerate(large_result):
                day_data = MOCK_OMER_DAY.copy()
                day_data['day'] = i + 1
                day.to_dict.return_value = day_data
            
            mock_range.return_value = large_result
            
            result = self.runner.invoke(cli, [
                'range',
                '--start-date', '2024-04-01',
                '--end-date', '2024-06-30'
            ])
            
            assert result.exit_code == 0
            assert "Found 49 Omer days" in result.output


# Additional test utilities
class TestCLIUtilities:
    """Test CLI utility functions"""
    
    def test_format_omer_day_edge_cases(self):
        """Test format_omer_day with edge cases"""
        # Test with minimal data
        minimal_data = {
            'day': 1,
            'week': 1,
            'day_of_week': 1,
            'text': 'היום יום אחד לעומר'
        }
        
        formatted = format_omer_day(minimal_data)
        assert "Day 1 of the Omer" in formatted
        assert "היום יום אחד לעומר" in formatted

    def test_display_blessing_edge_cases(self, capsys):
        """Test display_blessing with edge cases"""
        # Test with minimal blessing data
        minimal_blessing = {
            'hebrew': 'ברוך אתה השם',
            'transliteration': 'Baruch atah Hashem',
            'english': 'Blessed are You, Hashem'
        }
        
        display_blessing(minimal_blessing)
        captured = capsys.readouterr()
        
        assert "ברוך אתה השם" in captured.out
        assert "Baruch atah Hashem" in captured.out

    def test_format_functions_with_none_values(self):
        """Test format functions with None values"""
        data_with_nones = {
            'day': 1,
            'week': 1,
            'day_of_week': 1,
            'text': 'היום יום אחד לעומר',
            'transliteration': None,
            'english_translation': None
        }
        
        # Should not raise exception
        formatted = format_omer_day(data_with_nones)
        assert "Day 1 of the Omer" in formatted


if __name__ == '__main__':
    pytest.main([__file__, '-v'])