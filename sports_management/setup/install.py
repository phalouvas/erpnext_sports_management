# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.permissions import add_permission, update_permission_property

DEFAULT_ROLE_PROFILES = {
	"Sports": [
		"Sports User",
	]	
}

def after_install():
	create_domain()
	create_user_roles()
	create_default_role_profiles()
	add_permissions()

# Create domain Sports Management
def create_domain():
	# Check if the domain exists
	if not frappe.db.exists("Domain", "Sports Management"):
		domain = frappe.get_doc({
			"doctype": "Domain",
			"domain_name": "Sports Management"
		})
		domain.insert(ignore_permissions=True)

def create_user_roles():
	# Check if the role exists
	if not frappe.db.exists("Role", "Sports User"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Sports User",
			"desk_access": 1,
			"restrict_to_domain": "Sports Management"
		})
		role.insert(ignore_permissions=True)

	# Check if the role exists
	if not frappe.db.exists("Role", "Sports Manager"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Sports Manager",
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
	 
# Remove permissions, roles, role profiles and domain upon uninstall
def after_uninstall():
	remove_permissions()
	remove_default_role_profiles()
	remove_user_roles()
	remove_domain()

def remove_permissions():
	for doctype in ("Contact", "Address", "Company"):
		role = "Sports User"
		frappe.call("frappe.core.page.permission_manager.permission_manager.remove", doctype=doctype, role=role, permlevel=0)

		role = "Sports Manager"
		frappe.call("frappe.core.page.permission_manager.permission_manager.remove", doctype=doctype, role=role, permlevel=0)

def remove_user_roles():
	# Check if the role exists
	if frappe.db.exists("Role", "Sports User"):
		frappe.delete_doc("Role", "Sports User", ignore_permissions=True)

	# Check if the role exists
	if frappe.db.exists("Role", "Sports Manager"):
		frappe.delete_doc("Role", "Sports Manager", ignore_permissions=True)

def remove_default_role_profiles():
	# Check if the role profile exists
	if frappe.db.exists("Role Profile", "Sports"):
		frappe.delete_doc("Role Profile", "Sports", ignore_permissions=True)

def remove_domain():
	# Check if the domain exists
	if frappe.db.exists("Domain", "Sports Management"):
		frappe.delete_doc("Domain", "Sports Management", ignore_permissions=True)
