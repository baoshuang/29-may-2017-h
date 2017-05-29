"""
Author: Saikumar Kalyankrishnan
Created: Feb 15th 2017
Description: Object Repository for Repositories Page
"""


class RepositoriesObjectRepo():
    def RepositoriesObjects(self, key):
        RepositoriesObjects = {'settings_repo': ".//nav//a[contains(text(), 'Repositories')]",
                               'page_repositories': ".//*[@id='page_repositories']/div/h1",
                               'repo_tab': "tabISO",
                               'FW_tab': "tabFirmware",
                               'OS_repos': ".//*[@id='tab-iso']/div/article/table/tbody/tr",
                               'os_repos_names': ".//*[@id='tab-iso']/div/article/table/tbody/tr/td[2]",
                               'FW_repos': ".//*[@id='firmwarepackageTable']/tbody/tr",
                               'Add_repo': "lnkCreate",
                               'repo_name': "name",
                               'pager': "pager-bundleTable-firmware",
                               'fw_bundle_page_title': ".//h4[contains(@class,'modal-title')]",
                               'bundles': ".//*[@id='bundleTable_firmware']/tbody/tr",
                               'next_button': ".//i[contains(@class, 'glyphicon-forward')]",
                               'btn_close_bundles': "btnCloseBundleForm",
                               'btn_close_edit_bundle': ".//form[@id='form_add_bundle']/following-sibling::footer//button[@id='btnCloseBundleForm']",
                               'modal_title': "modal-title",
                               'alert_danger': "alert-danger",
                               'dialog_box': ".//h4[text()='Success']",
                               'btn_close': ".//button[text()='Close']",
                               'repo_image_type': "imagetype",
                               'loading_in': ".//div[@class='modal fade loading in']",
                               'repo_path': "path",
                               'repo_UN': "username",
                               'repo_psw': "form_password",
                               'repo_TC': "btnTestConnection",
                               'repo_save': "submit_repository_form",
                               'repo_cancel': "cancel_repository_form",
                               'repo_action': ".//*[@id='tab-iso']/div/article/table/tbody/tr/td[6]/select",
                               'default_FW': "ddlDefaultFirmware",
                               'Add_FW': "new_firmwarepackage_link",
                               'FW_action': ".//*[@id='firmwarepackageTable']/tbody/tr[1]/td[5]/select",
                               'view_bundles': "lnkViewFirmwarePackageDetails",
                               'add_custom_bundle': "lnkAddBundle",
                               'bundle_name': "bundleName",
                               'bundle_description': "bundleDescription",
                               'device_type': "deviceType",
                               'device_model': "deviceModel",
                               'bundle_version': "bundleVersion",
                               'criticality': "criticality",
                               'fw_package_file': "firmwarepackagefile",
                               'fw_bundle_save': "firmwareBundleSubmit",
                               'user_bundles': ".//table[@id='userBundles']/tbody/tr",
                               'catalog_FTP': "getLatestFromDell",
                               'catalog_local': "networkpath",
                               'local_file_path': "filepath",
                               'local_UN': "username",
                               'local_psw': "password",
                               'catalog_file': "createfromfile",
                               'file_browse_path': "idLocationFileUpload",
                               'set_catalog_default': "makeDefault",
                               'FW_TC': "btnTestFWConnection",
                               'FW_save': "firmwarepackageSubmit",
                               'FW_cancel': "btnCancel",
                               'close': "btnClose",
                               'spinner': ".//*[@id='tab-iso']//spinner",
                               'OS_col_names': ".//*[@id='tab-iso']/div/article/table/thead/tr/th",
                               'current_file_name': ".//*[@id='form_add_bundle']/fieldset/div[7]/div/span",
                               'btnConfirm': "btnConfirm",
                               'spinning_wheel': ".//spinner[@class='ng-scope ng-isolate-scope']/*[name()='svg']",
                               'lnkRemoveUserBundle': ".//*[@id='lnkRemoveUserBundle']",
                               'copying': ".//span[@ng-switch-when='copying']",
                               }
        return RepositoriesObjects.get(key)
