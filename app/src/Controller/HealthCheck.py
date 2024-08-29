import src.Omada.Controller as Controller

class HealthCheck:
    
    @staticmethod
    def get_status():
        return Controller.HealthCheck.get()