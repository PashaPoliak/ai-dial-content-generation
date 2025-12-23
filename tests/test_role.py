import pytest
from task._models.role import Role


class TestRoleModel:
    

    def test_role_values(self):
        
        assert Role.SYSTEM.value == "system"
        assert Role.USER.value == "user"
        assert Role.AI.value == "assistant"

    def test_role_creation_from_value(self):
        
        assert Role("system") == Role.SYSTEM
        assert Role("user") == Role.USER
        assert Role("assistant") == Role.AI

    def test_role_string_representation(self):
        
        assert str(Role.SYSTEM) == "system"
        assert str(Role.USER) == "user"
        assert str(Role.AI) == "assistant"

    def test_role_equality(self):
        
        assert Role.SYSTEM == Role("system")
        assert Role.USER == Role("user")
        assert Role.AI == Role("assistant")
        assert Role.SYSTEM != Role.USER

    def test_invalid_role_creation(self):
        
        with pytest.raises(ValueError):
            Role("invalid_role")

    def test_role_in_list(self):
        
        roles = [Role.SYSTEM, Role.USER, Role.AI]
        
        assert Role.SYSTEM in roles
        assert Role.USER in roles
        assert Role.AI in roles
        assert Role("system") in roles


    def test_role_serialization(self):
        
        assert Role.SYSTEM.value == "system"
        assert Role.USER.value == "user"
        assert Role.AI.value == "assistant"

    def test_role_case_sensitivity(self):
        
        with pytest.raises(ValueError):
            Role("System")
        
        with pytest.raises(ValueError):
            Role("USER")
        
        with pytest.raises(ValueError):
            Role("Assistant")

    def test_role_consistency(self):
        
        role1 = Role.USER
        role2 = Role.USER
        
        assert role1 is role2
        assert role1.value == role2.value
        assert str(role1) == str(role2)
