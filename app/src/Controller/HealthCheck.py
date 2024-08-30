import src.Omada.Controller as Controller
import src.Model as Model

class HealthCheck:
    
    @staticmethod
    def get_status() -> Model.HealthCheck:
        result = Controller.HealthCheck.get()
        return Model.HealthCheck(
            **result
        )