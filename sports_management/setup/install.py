# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.permissions import add_permission, update_permission_property

DEFAULT_ROLE_PROFILES = {
	"Sports": [
		"Sports User",
		"Customer",
	]	
}

def after_install():
	create_user_roles()
	create_default_role_profiles()
	add_permissions()

def create_user_roles():
	# Check if the role exists
	if not frappe.db.exists("Role", "Sports User"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Sports User",
			"desk_access": 0,
			"restrict_to_domain": ""
		})
		role.insert(ignore_permissions=True)
		role.desk_access = 0
		role.save()

	# Check if the role exists
	if not frappe.db.exists("Role", "Sports Manager"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Sports Manager",
			"desk_access": 1,
			"restrict_to_domain": ""
		})
		role.insert(ignore_permissions=True)

	# Check if the role Sports Referee exists
	if not frappe.db.exists("Role", "Sports Referee"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Sports Referee",
			"desk_access": 1,
			"restrict_to_domain": ""
		})
		role.insert(ignore_permissions=True)
	
def create_default_role_profiles():
	
	# Check if the role profile exists
	if not frappe.db.exists("Role Profile", "Sports"):
		for role_profile_name, roles in DEFAULT_ROLE_PROFILES.items():
			role_profile = frappe.new_doc("Role Profile")
			role_profile.role_profile = role_profile_name
			for role in roles:
				role_profile.append("roles", {"role": role})

			role_profile.insert(ignore_permissions=True)

def add_permissions():

	for doctype in ("Contact", "Address"):
		role = "Sports User"
		add_permission(doctype, role, 0)
		update_permission_property(doctype, role, 0, "if_owner", 1)
		update_permission_property(doctype, role, 0, "create", 1)
		update_permission_property(doctype, role, 0, "write", 1)
		update_permission_property(doctype, role, 0, "delete", 1)
		update_permission_property(doctype, role, 0, "read", 1)
		update_permission_property(doctype, role, 0, "report", 1)
		update_permission_property(doctype, role, 0, "print", 1)
		update_permission_property(doctype, role, 0, "share", 1)

		role = "Sports Manager"
		add_permission(doctype, role, 0)
		update_permission_property(doctype, role, 0, "if_owner", 1)
		update_permission_property(doctype, role, 0, "create", 1)
		update_permission_property(doctype, role, 0, "write", 1)
		update_permission_property(doctype, role, 0, "delete", 1)
		update_permission_property(doctype, role, 0, "read", 1)
		update_permission_property(doctype, role, 0, "report", 1)
		update_permission_property(doctype, role, 0, "print", 1)
		update_permission_property(doctype, role, 0, "share", 1)

	doctype = "Company"
	add_permission(doctype, role, 0)
	update_permission_property(doctype, role, 0, "if_owner", 0)
	update_permission_property(doctype, role, 0, "create", 0)
	update_permission_property(doctype, role, 0, "write", 0)
	update_permission_property(doctype, role, 0, "delete", 0)
	update_permission_property(doctype, role, 0, "read", 1)
	update_permission_property(doctype, role, 0, "report", 0)
	update_permission_property(doctype, role, 0, "print", 0)
	update_permission_property(doctype, role, 0, "share", 0)
	update_permission_property(doctype, role, 0, "export", 1)

	add_permission(doctype, "Sports Manager", 0)
	add_permission(doctype, role, 0)
	update_permission_property(doctype, role, 0, "if_owner", 0)
	update_permission_property(doctype, role, 0, "create", 0)
	update_permission_property(doctype, role, 0, "write", 0)
	update_permission_property(doctype, role, 0, "delete", 0)
	update_permission_property(doctype, role, 0, "read", 1)
	update_permission_property(doctype, role, 0, "report", 0)
	update_permission_property(doctype, role, 0, "print", 0)
	update_permission_property(doctype, role, 0, "share", 0)
	update_permission_property(doctype, role, 0, "export", 1)
