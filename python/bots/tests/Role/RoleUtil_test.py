
from common.Util import Util
from common.models.KfpRole import KfpRole
from common.RoleUtil import RoleUtil
from common.KFP_DB import KfpDb

class TestRoleUtil():
    def setup_method(self, method):
        self.database = KfpDb(":memory:")
        pass
    def teardown_method(self, method):
        self.database.teardown()
        pass

    def test_updateRoleCreateNewOne(self):
        role: KfpRole = RoleUtil.updateRole(123, 321, "testing", "0x000345")
        
        assert role.guild_id == 123
        assert role.role_id == 321
        assert role.role_name == "testing"
        assert role.color == "0x000345"

    def test_updateRoleUpdateOldOne(self):
        RoleUtil.updateRole(123, 321, "testing", "0x000345")
        role: KfpRole = RoleUtil.updateRole(123, 321, "onetwothree", "0x000543")

        assert role.role_name == "onetwothree"
        assert role.color == "0x000543"

    def test_updateKfpRoleLevelZero(self):
        RoleUtil.updateRole(123, 321, "testing", "0x000345")
        role: KfpRole = RoleUtil.getRole(123, 321)

        assert role.level == 0

    def test_updateKfpRoleLevelSuccess(self):
        RoleUtil.updateRole(123, 321, "testing", "0x000345")
        role: KfpRole = RoleUtil.getRole(123, 321)
        RoleUtil.updateKfpRoleLevel(role, 20)

        assert role.level == 20

    def test_getCurrentRolesEmpty(self):
        roleList = RoleUtil.getCurrentRoles(123)
        assert len(roleList) == 0

    
    def test_getCurrentRolesSuccess(self):
        role1 = RoleUtil.updateRole(123, 321, "testing", "0x000345")
        role2 = RoleUtil.updateRole(123, 123, "onetwothree", "0x000543")
        roleList = RoleUtil.getCurrentRoles(123)
        assert len(roleList) == 2
        assert roleList[0] == role1
        assert roleList[1] == role2
    
    def test_getCurrentRolesSuccess_level(self):
        role1 = RoleUtil.updateRole(123, 100, "first", "0x000345", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role1, 0)
        role2 = RoleUtil.updateRole(123, 101, "second", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role2, 20)
        role3 = RoleUtil.updateRole(123, 102, "third", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role3, 40)
        role4 = RoleUtil.updateRole(123, 103, "fourth", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role4, 60)
        role5 = RoleUtil.updateRole(123, 104, "fifth", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role5, 80)
        role6 = RoleUtil.updateRole(123, 105, "sixth", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role6, 100)
        role = RoleUtil.getKfpRoleFromLevel(123, 80)

        assert role == role5


    def test_getRoleBeforeLevel(self):
        role1 = RoleUtil.updateRole(123, 321, "testing", "0x000345", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role1, 10)
        role2 = RoleUtil.updateRole(123, 123, "onetwothree", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role2, 20)

        role = RoleUtil.getKfpRolesBeforeLevel(123, 9)
        assert len(role) == 0
        role = RoleUtil.getKfpRolesBeforeLevel(123, 11)
        assert role[0] == role1
        role = RoleUtil.getKfpRolesBeforeLevel(123, 20)
        assert role[0] == role1
        role = RoleUtil.getKfpRolesBeforeLevel(123, 21)
        assert role[0] == role2
        assert role[1] == role1

    def test_getRoleFromLevel(self):
        role0 = RoleUtil.updateRole(123, 100, "other roles", "0x000345")
        RoleUtil.updateKfpRoleLevel(role0, 0)
        role1 = RoleUtil.updateRole(123, 321, "testing", "0x000345", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role1, 10)
        role2 = RoleUtil.updateRole(123, 123, "onetwothree", "0x000543", Util.RoleCategory.KFP_DEFAULT)
        RoleUtil.updateKfpRoleLevel(role2, 20)

        role = RoleUtil.getKfpRoleFromLevel(123, 9)
        assert not role
        role = RoleUtil.getKfpRoleFromLevel(123, 11)
        assert role == role1 
        role = RoleUtil.getKfpRoleFromLevel(123, 20)
        assert role == role2 