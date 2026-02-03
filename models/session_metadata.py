# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

"""
Session Metadata Data Model
Contains all test session setup information entered at login

Fields are organized into 3 categories:
1. Ürün Bilgileri (Product Information) - goes to Excel report
2. Yazılım Bilgileri (Software Information) - goes to Excel report
3. Cihaz Kalibrasyonları (Device Calibrations) - goes to Excel report
4. Oturum Bilgileri (Session Info) - İstasyon and SİP for UI only, NOT in Excel
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from datetime import date, datetime


@dataclass
class SessionMetadata:
    """
    Complete test session metadata.
    
    All fields have defaults for easy initialization.
    Calibration dates are stored as date objects for easy comparison.
    """
    
    # =========================================================================
    # ÜRÜN BİLGİLERİ (Product Information) - Goes to Excel Report
    # =========================================================================
    stok_no: str = ""
    opsiyonel_stok_no: str = ""
    tanim: str = ""  # Tanım (Description)
    teu_udk: str = ""
    seri_no: str = ""
    revizyon_261: str = ""  # 261 revizyonu
    test_donanimi_revizyon: str = ""  # Test Donanımı Revizyon
    test_yazilimi_revizyon: str = ""  # Test Yazılımı Revizyonu
    is_tipi_no: str = ""  # İş Tipi No
    
    # =========================================================================
    # YAZILIM BİLGİLERİ (Software Information) - Goes to Excel Report
    # =========================================================================
    kay_yazilimi_versiyon: str = ""  # KAY Yazılımı Versiyon No
    sky_yazilimi_versiyon: str = ""  # SKY Yazılımı Versiyon No
    
    # =========================================================================
    # CİHAZ KALİBRASYONLARI (Device Calibrations) - Goes to Excel Report
    # Stored as ISO date strings (YYYY-MM-DD) for JSON serialization
    # =========================================================================
    fluke_esa620_kalibrasyon: str = ""  # FLUKE ESA620 kalibrasyon bitiş tarihi
    italsea_7proglcd_kalibrasyon: str = ""  # ITALSEA 7PROGLCD kalibrasyon bitiş tarihi
    geratech_kalibrasyon: str = ""  # Geratech kalibrasyon bitiş tarihi
    iba_magicmax_kalibrasyon: str = ""  # IBA MagicMax kalibrasyon bitiş tarihi
    iba_primus_a_kalibrasyon: str = ""  # IBA Primus A kalibrasyon bitiş tarihi
    
    # =========================================================================
    # OTURUM BİLGİLERİ (Session Info) - UI Header ONLY, NOT in Excel Report
    # =========================================================================
    istasyon: str = ""  # İstasyon (Station) - for UI header only
    sip_code: str = ""  # SİP Kodu - for UI header only
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.
        
        Returns:
            Dictionary with all fields
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMetadata':
        """
        Create SessionMetadata from dictionary.
        
        Args:
            data: Dictionary with metadata fields
            
        Returns:
            SessionMetadata instance
        """
        # Filter only known fields to avoid TypeError
        known_fields = {
            'stok_no', 'opsiyonel_stok_no', 'tanim', 'teu_udk', 'seri_no',
            'revizyon_261', 'test_donanimi_revizyon', 'test_yazilimi_revizyon',
            'is_tipi_no', 'kay_yazilimi_versiyon', 'sky_yazilimi_versiyon',
            'fluke_esa620_kalibrasyon', 'italsea_7proglcd_kalibrasyon',
            'geratech_kalibrasyon', 'iba_magicmax_kalibrasyon',
            'iba_primus_a_kalibrasyon', 'istasyon', 'sip_code'
        }
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered_data)
    
    def get_excel_data(self) -> Dict[str, Any]:
        """
        Get only the fields that should appear in Excel report.
        Excludes İstasyon and SİP (UI-only fields).
        
        Returns:
            Dictionary with Excel-exportable fields
        """
        data = self.to_dict()
        # Remove UI-only fields
        data.pop('istasyon', None)
        data.pop('sip_code', None)
        return data
    
    def get_calibration_status(self, field_name: str) -> str:
        """
        Check calibration date status.
        
        Args:
            field_name: Name of calibration field
            
        Returns:
            'valid' (>30 days), 'warning' (<=30 days), 'expired', or 'empty'
        """
        date_str = getattr(self, field_name, "")
        if not date_str:
            return 'empty'
        
        try:
            cal_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = date.today()
            days_remaining = (cal_date - today).days
            
            if days_remaining < 0:
                return 'expired'
            elif days_remaining <= 30:
                return 'warning'
            else:
                return 'valid'
        except ValueError:
            return 'empty'
    
    def get_all_calibration_statuses(self) -> Dict[str, str]:
        """
        Get status of all calibration dates.
        
        Returns:
            Dictionary mapping field name to status
        """
        calibration_fields = [
            'fluke_esa620_kalibrasyon',
            'italsea_7proglcd_kalibrasyon',
            'geratech_kalibrasyon',
            'iba_magicmax_kalibrasyon',
            'iba_primus_a_kalibrasyon'
        ]
        return {field: self.get_calibration_status(field) for field in calibration_fields}
    
    def has_expired_calibrations(self) -> bool:
        """
        Check if any calibration is expired.
        
        Returns:
            True if any calibration is expired
        """
        statuses = self.get_all_calibration_statuses()
        return 'expired' in statuses.values()
    
    def format_date_for_display(self, field_name: str) -> str:
        """
        Format a date field for display (DD/MM/YYYY).
        
        Args:
            field_name: Name of date field
            
        Returns:
            Formatted date string or empty string
        """
        date_str = getattr(self, field_name, "")
        if not date_str:
            return ""
        
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            return date_str
    
    def __repr__(self) -> str:
        return (f"SessionMetadata(stok_no={self.stok_no}, "
                f"seri_no={self.seri_no}, "
                f"istasyon={self.istasyon})")