class RouteTool:
    def __init__(self):
        self.code_owner_map = {
            "app/auth.py": "@auth-team",
            "app/payments.py": "@payments-team",
            "app/email/utils.py": "@platform-team",
            "app/upload/handler.py": "@infra-team",
            "app/dashboard/*.py": "@dashboard-team"
        }

    """
    Replace this static map with a call to Github
    """

    def get_code_owner(self, filepath: str) -> str:
        for path_pattern, owner in self.code_owner_map.items():
            if path_pattern.endswith("*.py"):
                base = path_pattern.replace("*.py", "")
                if filepath.startswith(base):
                    return owner
            elif filepath == path_pattern:
                return owner
        return ""

