# -*- coding: utf-8 -*-

"""
Authentication Manager
3-Role System: Admin, Operator, Developer

Features:
- Load users from data/users.json (organized by role folders)
- Admin: Can navigate back, edit results, export
- Operator: Basic test execution only (no password)
- Developer: All admin rights + can edit test steps (future)
"""
import hashlib
import json
import os
from typing import Optional, Dict, List, Any
from pathlib import Path
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class UserRole:
    """
    3 User role types with different permission levels.
    
    Hierarchy:
    1. DEVELOPER - All admin rights + can edit test steps (future)
    2. ADMIN - Can navigate back, edit results, manage users
    3. OPERATOR - Basic test execution only
    """
    ADMIN = "admin"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    
    # Display names (Turkish)
    DISPLAY_NAMES = {
        ADMIN: "Yönetici",
        OPERATOR: "Operatör",
        DEVELOPER: "Geliştirici"
    }
    
    # Roles that can navigate backward
    BACKWARD_NAV_ROLES = [ADMIN, DEVELOPER]
    
    # Roles that can edit submitted results
    EDIT_ROLES = [ADMIN, DEVELOPER]
    
    # Roles that can export reports
    EXPORT_ROLES = [ADMIN, DEVELOPER]
    
    # Roles that can edit test steps (future feature)
    EDIT_STEPS_ROLES = [DEVELOPER]
    
    # Roles that require password
    PASSWORD_REQUIRED_ROLES = [ADMIN, DEVELOPER]


class AuthManager:
    """
    3-Role Authentication Manager.
    
    Roles:
    - ADMIN: Can navigate back, edit results, export reports
    - OPERATOR: Basic test execution only (no password required)
    - DEVELOPER: All admin rights + can edit test steps (future)
    
    Users are organized in folders/lists in users.json:
    - users.admins[]
    - users.operators[]
    - users.developers[]
    
    Usage:
        auth = AuthManager()
        
        # Operator login (no password)
        auth.login_as_operator("op1")
        
        # Admin/Developer login (with password)
        if auth.authenticate("admin", "admin123"):
            print(f"Welcome {auth.get_display_name()}")
    """
    
    # Path to users file
    USERS_FILE = "data/users.json"
    
    def __init__(self):
        """Initialize AuthManager and load users from file."""
        self.current_user: Optional[Dict] = None
        
        # Users organized by role
        self.admins: List[Dict] = []
        self.operators: List[Dict] = []
        self.developers: List[Dict] = []
        
        # Role permissions
        self.roles: Dict[str, Dict] = {}
        
        # Try to load users from file
        self._load_users_from_file()
        
        total_users = len(self.admins) + len(self.operators) + len(self.developers)
        logger.info(f"AuthManager initialized: {len(self.admins)} admins, {len(self.operators)} operators, {len(self.developers)} developers")
    
    # ========================================================================
    # USER LOADING
    # ========================================================================
    
    def _load_users_from_file(self) -> bool:
        """
        Load users from data/users.json file.
        
        JSON structure:
        {
            "users": {
                "admins": [...],
                "operators": [...],
                "developers": [...]
            },
            "roles": {...}
        }
        
        Returns:
            True if loaded successfully, False otherwise
        """
        # Try multiple paths
        possible_paths = [
            Path(self.USERS_FILE),
            Path(__file__).parent.parent / "data" / "users.json",
            Path.cwd() / "data" / "users.json"
        ]
        
        users_file = None
        for path in possible_paths:
            if path.exists():
                users_file = path
                break
        
        if users_file is None:
            logger.warning("users.json not found, using default users")
            self._create_default_users()
            return False
        
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            users_data = data.get('users', {})
            
            # Load users by role folder
            self.admins = [u for u in users_data.get('admins', []) if u.get('active', True)]
            self.operators = [u for u in users_data.get('operators', []) if u.get('active', True)]
            self.developers = [u for u in users_data.get('developers', []) if u.get('active', True)]
            
            # Add role field to each user
            for user in self.admins:
                user['role'] = UserRole.ADMIN
            for user in self.operators:
                user['role'] = UserRole.OPERATOR
            for user in self.developers:
                user['role'] = UserRole.DEVELOPER
            
            # Load role permissions
            self.roles = data.get('roles', {})
            
            logger.info(f"Loaded users from {users_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load users.json: {e}")
            self._create_default_users()
            return False
    
    def _create_default_users(self):
        """Create default users if users.json doesn't exist."""
        self.admins = [
            {
                "username": "admin",
                "password_hash": self._hash_password("admin123"),
                "display_name": "Yönetici",
                "employee_id": "ADM001",
                "role": UserRole.ADMIN,
                "active": True
            }
        ]
        
        self.operators = [
            {
                "username": "operator",
                "password_hash": "",
                "display_name": "Operatör",
                "employee_id": "OP000",
                "role": UserRole.OPERATOR,
                "active": True
            }
        ]
        
        self.developers = [
            {
                "username": "dev",
                "password_hash": self._hash_password("dev123"),
                "display_name": "Geliştirici",
                "employee_id": "DEV001",
                "role": UserRole.DEVELOPER,
                "active": True
            }
        ]
        
        self.roles = {
            UserRole.ADMIN: {"can_navigate_back": True, "can_edit_results": True, "can_edit_test_steps": False},
            UserRole.OPERATOR: {"can_navigate_back": False, "can_edit_results": False, "can_edit_test_steps": False},
            UserRole.DEVELOPER: {"can_navigate_back": True, "can_edit_results": True, "can_edit_test_steps": True}
        }
        
        logger.info("Created default users (1 admin, 1 operator, 1 developer)")
    
    # ========================================================================
    # AUTHENTICATION
    # ========================================================================
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user with username and password.
        Used for Admin and Developer logins.
        
        Args:
            username: Username to authenticate
            password: Password to check
            
        Returns:
            True if authenticated successfully
        """
        # Find user in all lists
        user = self._find_user(username)
        
        if user is None:
            logger.warning(f"Authentication failed: User '{username}' not found")
            return False
        
        # Check if user is active
        if not user.get('active', True):
            logger.warning(f"Authentication failed: User '{username}' is inactive")
            return False
        
        # Check password
        password_hash = self._hash_password(password)
        stored_hash = user.get('password_hash', '')
        
        if password_hash != stored_hash:
            logger.warning(f"Authentication failed: Invalid password for '{username}'")
            return False
        
        # Set current user
        self.current_user = user.copy()
        logger.info(f"User authenticated: {user['display_name']} ({user['role']})")
        
        return True
    
    def authenticate_by_password_only(self, password: str) -> bool:
        """
        Authenticate using only password (for quick admin/dev login).
        Searches admins and developers for matching password.
        
        Args:
            password: Password to check
            
        Returns:
            True if authenticated successfully
        """
        password_hash = self._hash_password(password)
        
        # Search admins and developers (not operators - they don't have passwords)
        for user in self.admins + self.developers:
            if not user.get('active', True):
                continue
                
            if user.get('password_hash') == password_hash:
                self.current_user = user.copy()
                logger.info(f"User authenticated by password: {user['display_name']}")
                return True
        
        # Fallback: check default admin password
        if password == config.DEFAULT_ADMIN_PASSWORD:
            self.current_user = {
                'role': UserRole.ADMIN,
                'username': 'admin',
                'display_name': 'Yönetici',
                'employee_id': 'ADM001'
            }
            logger.info("Admin authenticated with default password")
            return True
        
        logger.warning("Authentication failed: No matching password found")
        return False
    
    def login_as_operator(self, username: str = None):
        """
        Login as operator (no password required).
        
        Args:
            username: Specific operator username, or None for default
        """
        if username:
            # Find specific operator
            for op in self.operators:
                if op.get('username') == username and op.get('active', True):
                    self.current_user = op.copy()
                    logger.info(f"Logged in as operator: {op['display_name']}")
                    return
        
        # Use first active operator or create default
        if self.operators:
            self.current_user = self.operators[0].copy()
            logger.info(f"Logged in as operator: {self.current_user['display_name']}")
        else:
            self.current_user = {
                'role': UserRole.OPERATOR,
                'username': 'operator',
                'display_name': 'Operatör',
                'employee_id': 'OP000'
            }
            logger.info("Logged in as default operator")
    
    # Alias for backward compatibility
    def authenticate_as_operator(self, username: str = None):
        """Alias for login_as_operator."""
        self.login_as_operator(username)
    
    def logout(self):
        """Clear current user session."""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user.get('display_name')}")
        self.current_user = None
    
    # ========================================================================
    # USER LOOKUP
    # ========================================================================
    
    def _find_user(self, username: str) -> Optional[Dict]:
        """
        Find user by username in all role lists.
        
        Args:
            username: Username to find
            
        Returns:
            User dict or None
        """
        username_lower = username.lower()
        
        # Search all role lists
        for user in self.admins + self.operators + self.developers:
            if user.get('username', '').lower() == username_lower:
                return user
        return None
    
    def get_all_users(self, active_only: bool = True) -> List[Dict]:
        """
        Get list of all users from all roles.
        
        Args:
            active_only: If True, return only active users
            
        Returns:
            List of user dictionaries
        """
        all_users = self.admins + self.operators + self.developers
        
        if active_only:
            return [u for u in all_users if u.get('active', True)]
        return all_users
    
    def get_admins(self) -> List[Dict]:
        """Get list of all admin users."""
        return [u for u in self.admins if u.get('active', True)]
    
    def get_operators(self) -> List[Dict]:
        """Get list of all operator users."""
        return [u for u in self.operators if u.get('active', True)]
    
    def get_developers(self) -> List[Dict]:
        """Get list of all developer users."""
        return [u for u in self.developers if u.get('active', True)]
    
    # ========================================================================
    # CURRENT USER INFO
    # ========================================================================
    
    def get_role(self) -> str:
        """Get current user's role."""
        if self.current_user:
            return self.current_user.get('role', UserRole.OPERATOR)
        return UserRole.OPERATOR
    
    def get_display_name(self) -> str:
        """Get current user's display name."""
        if self.current_user:
            return self.current_user.get('display_name', 'Kullanıcı')
        return "Kullanıcı"
    
    def get_username(self) -> str:
        """Get current user's username."""
        if self.current_user:
            return self.current_user.get('username', '')
        return ""
    
    def get_employee_id(self) -> str:
        """Get current user's employee ID."""
        if self.current_user:
            return self.current_user.get('employee_id', '')
        return ""
    
    def get_department(self) -> str:
        """Get current user's department."""
        if self.current_user:
            return self.current_user.get('department', '')
        return ""
    
    # ========================================================================
    # PERMISSION CHECKS
    # ========================================================================
    
    def is_admin(self) -> bool:
        """Check if current user is admin."""
        return self.get_role() == UserRole.ADMIN
    
    def is_operator(self) -> bool:
        """Check if current user is operator."""
        return self.get_role() == UserRole.OPERATOR
    
    def is_developer(self) -> bool:
        """Check if current user is developer."""
        return self.get_role() == UserRole.DEVELOPER
    
    def can_navigate_back(self) -> bool:
        """
        Check if current user can navigate to previous steps.
        Admins and Developers can navigate back.
        """
        role = self.get_role()
        
        # Check role permissions from loaded data
        if role in self.roles:
            return self.roles[role].get('can_navigate_back', False)
        
        # Fallback to hardcoded list
        return role in UserRole.BACKWARD_NAV_ROLES
    
    def can_edit_results(self) -> bool:
        """
        Check if current user can edit submitted results.
        Admins and Developers can edit results.
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get('can_edit_results', False)
        
        return role in UserRole.EDIT_ROLES
    
    def can_export(self) -> bool:
        """
        Check if current user can export reports.
        Admins and Developers can export.
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get('can_export', True)
        
        return role in UserRole.EXPORT_ROLES
    
    def can_edit_test_steps(self) -> bool:
        """
        Check if current user can edit test steps (Developer mode).
        Only Developers can edit test steps.
        
        Future feature: UI for adding/editing test steps.
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get('can_edit_test_steps', False)
        
        return role in UserRole.EDIT_STEPS_ROLES
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if current user has a specific permission.
        
        Args:
            permission: Permission name (e.g., 'can_navigate_back', 'can_edit_test_steps')
            
        Returns:
            True if user has the permission
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get(permission, False)
        
        return False
    
    # ========================================================================
    # PASSWORD UTILITIES
    # ========================================================================
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash password using MD5 (for demo compatibility).
        
        Note: Use SHA-256 in production!
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.md5(password.encode()).hexdigest()
    
    @staticmethod
    def hash_password_sha256(password: str) -> str:
        """
        Hash password using SHA-256 (recommended for production).
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ========================================================================
    # USER MANAGEMENT (Future)
    # ========================================================================
    
    def add_user(self, username: str, password: str, role: str, 
                 display_name: str, employee_id: str = "", 
                 department: str = "") -> bool:
        """
        Add a new user (for future admin panel).
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            role: User role
            display_name: Display name
            employee_id: Employee ID
            department: Department name
            
        Returns:
            True if user added successfully
        """
        # Check if username exists
        if self._find_user(username):
            logger.warning(f"Cannot add user: '{username}' already exists")
            return False
        
        new_user = {
            "username": username,
            "password_hash": self._hash_password(password),
            "role": role,
            "display_name": display_name,
            "employee_id": employee_id,
            "department": department,
            "active": True
        }
        
        self.users.append(new_user)
        logger.info(f"User added: {display_name} ({role})")
        
        return True
    
    def save_users_to_file(self) -> bool:
        """
        Save current users list to JSON file.
        
        Returns:
            True if saved successfully
        """
        try:
            data = {
                "version": "1.0",
                "users": self.users,
                "roles": self.roles
            }
            
            with open(self.USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Users saved to {self.USERS_FILE}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
            return False