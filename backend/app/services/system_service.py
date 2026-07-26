class SystemService:
    """
    System application service.
    """

    def get_status(self) -> dict:
        return {
            "application": "Vertex Nurture",
            "status": "running",
            "version": "0.1.0",
        }