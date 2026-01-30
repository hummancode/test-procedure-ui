"""
Excel Exporter
Exports test results to formatted Excel files
"""
from typing import Optional, List
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from models.test_session import TestSession
from models.enums import TestStatus
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExcelExporter:
    """
    Exports test session data to formatted Excel files.
    
    Features:
    - Session metadata (stock number, serial, station, SIP)
    - Step-by-step results with status, duration, and comments
    - Color-coded pass/fail status
    - Professional formatting
    - Auto-column sizing
    """
    
    # Excel styling constants
    HEADER_FILL = PatternFill(start_color="1a237e", end_color="1a237e", fill_type="solid")
    HEADER_FONT = Font(color="FFFFFF", bold=True, size=12)
    
    PASS_FILL = PatternFill(start_color="C8E6C9", end_color="C8E6C9", fill_type="solid")
    FAIL_FILL = PatternFill(start_color="FFCDD2", end_color="FFCDD2", fill_type="solid")
    NA_FILL = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
    
    BORDER_THIN = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    def __init__(self):
        """Initialize the Excel exporter"""
        logger.info("ExcelExporter initialized")
    
    def export_session(self, session: TestSession, output_path: str) -> bool:
        """
        Export test session to Excel file.
        
        Args:
            session: TestSession to export
            output_path: Full path where Excel file should be saved
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            # Create workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Test Sonuçları"
            
            # Write content
            current_row = 1
            current_row = self._write_header_section(ws, session, current_row)
            current_row += 2  # Add spacing
            current_row = self._write_results_table(ws, session, current_row)
            
            # Auto-adjust column widths
            self._auto_size_columns(ws)
            
            # Save file
            wb.save(output_path)
            
            logger.info(f"Excel file exported successfully to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export Excel file: {e}")
            return False
    
    def _write_header_section(self, ws, session: TestSession, start_row: int) -> int:
        """
        Write session metadata header section.
        
        Returns:
            Next available row number
        """
        row = start_row
        
        # Title
        ws.merge_cells(f'A{row}:G{row}')
        cell = ws[f'A{row}']
        cell.value = "TEST PROSEDÜRÜ RAPORU"
        cell.font = Font(size=16, bold=True, color="1a237e")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        row += 2
        
        # Session info
        info_data = [
            ("STOK NO:", session.stock_number),
            ("SERİ NO:", session.serial_number),
            ("İSTASYON:", session.station_number),
            ("SİP KODU:", session.sip_code),
            ("BAŞLANGIÇ:", session.start_time.strftime(config.DATETIME_FORMAT) if session.start_time else "---"),
            ("BİTİŞ:", session.end_time.strftime(config.DATETIME_FORMAT) if session.end_time else "Devam Ediyor"),
            ("SÜRE:", f"{session.duration_seconds // 60} dakika {session.duration_seconds % 60} saniye"),
            ("TAMAMLANMA:", f"%{session.get_completion_percentage():.0f}"),
            ("BAŞARILI:", str(session.get_passed_count())),
            ("BAŞARISIZ:", str(session.get_failed_count())),
        ]
        
        for label, value in info_data:
            ws[f'A{row}'] = label
            ws[f'A{row}'].font = Font(bold=True)
            ws[f'B{row}'] = value
            row += 1
        
        return row
    
    def _write_results_table(self, ws, session: TestSession, start_row: int) -> int:
        """
        Write test results table with step details.
        
        Returns:
            Next available row number
        """
        row = start_row
        
        # Table headers
        headers = [
            "Adım No",
            "Adım Adı",
            "Durum",
            "Başlangıç",
            "Süre (sn)",
            "Sonuç",
            "Yorum"
        ]
        
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col_idx)
            cell.value = header
            cell.font = self.HEADER_FONT
            cell.fill = self.HEADER_FILL
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = self.BORDER_THIN
        
        row += 1
        
        # Table data
        for step in session.steps:
            col_idx = 1
            
            # Step ID
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.step_id
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Step Name
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.name
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Status (with color coding)
            cell = ws.cell(row=row, column=col_idx)
            status_text, status_fill = self._get_status_display(step.status)
            cell.value = status_text
            cell.fill = status_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Start Time
            cell = ws.cell(row=row, column=col_idx)
            if step.start_time:
                cell.value = datetime.fromtimestamp(step.start_time).strftime(config.DATETIME_FORMAT)
            else:
                cell.value = "---"
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Duration
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.actual_duration if step.actual_duration is not None else "---"
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Result Value
            cell = ws.cell(row=row, column=col_idx)
            cell.value = self._format_result_value(step.result_value)
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Comment
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.comment if step.comment else ""
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            row += 1
        
        return row
    
    def _get_status_display(self, status: TestStatus) -> tuple:
        """
        Get display text and fill color for status.
        
        Returns:
            Tuple of (status_text, fill_color)
        """
        if status == TestStatus.PASSED:
            return ("BAŞARILI", self.PASS_FILL)
        elif status == TestStatus.FAILED:
            return ("BAŞARISIZ", self.FAIL_FILL)
        elif status == TestStatus.NOT_APPLICABLE:
            return ("UYGULANMAZ", self.NA_FILL)
        elif status == TestStatus.IN_PROGRESS:
            return ("DEVAM EDİYOR", PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid"))
        else:
            return ("BAŞLANMAMIŞ", self.NA_FILL)
    
    def _format_result_value(self, value) -> str:
        """Format result value for display"""
        if value is None:
            return "---"
        elif value in ["PASS", "GEÇTİ"]:
            return "GEÇTİ"
        elif value in ["FAIL", "KALDI"]:
            return "KALDI"
        else:
            return str(value)
    
    def _auto_size_columns(self, ws):
        """Auto-adjust column widths based on content"""
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            # Set width with some padding
            adjusted_width = min(max_length + 2, 50)  # Max 50 characters
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def generate_filename(self, session: TestSession, output_dir: str) -> str:
        """
        Generate Excel filename based on session data.
        
        Format: TestRaporu_<STATION>_<DATE>_<STOCK>.xlsx
        
        Args:
            session: TestSession object
            output_dir: Directory where file will be saved
            
        Returns:
            Full path to output file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stock = self._sanitize_filename(session.stock_number)
        station = self._sanitize_filename(session.station_number)
        
        filename = f"TestRaporu_{station}_{timestamp}_{stock}.xlsx"
        
        return str(Path(output_dir) / filename)
    
    def _sanitize_filename(self, name: str) -> str:
        """Remove invalid characters from filename"""
        # Keep only alphanumeric, hyphens, and underscores
        return ''.join(c if c.isalnum() or c in '-_' else '_' for c in name)