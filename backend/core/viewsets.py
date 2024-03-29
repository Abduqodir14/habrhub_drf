class MixedPermission:
    """Миксин permissions для action"""
    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except (KeyError, AttributeError):
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]