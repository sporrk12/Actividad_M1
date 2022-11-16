from ActividadM1.ModelCleaner import ModelCleaner
import time

def cleaner_robot_activity():

    # cantidad de agentes
    # dimension de matriz
    # dimension de matriz
    # porcentaje de celdas sucias
    model = ModelCleaner(15, 8, 8, 0.40)

    # cantidad de steps (máximo tiempo de ejecución)
    max_exec_time = 20

    model.initial_time = time.time()

    # cantidad de set
    for i in range(max_exec_time):
        model.step()
        print('Porcentaje de limpieza:', str(round(model.dirtyCellRatio() * 100, 2)) + '%')

    print(model.total_movements())

    model.final_time = time.time()

    model.program_execution_time()