import mesa
import random
import math
import time
import matplotlib as plt

class AgentCleanerRobot(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.amount_movements = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        # Dirección aleatoria disponible.
        new_position = self.random.choice(possible_steps)

        # Movimiento a la dirección seleccionada
        self.model.grid.move_agent(self, new_position)

    def clean(self):

        # Si está sucio se cambia
        if self.model.isDirty(self.pos):
            self.model.setDirty(self.pos)



    def step(self):

        # Revisión de limpieza
        if self.model.dirtyCellRatio() >= 0.99:
            self.model.final_time = time.time()
        else:

            self.move()
            self.clean()
            self.amount_movements = self.amount_movements + 1



class ModelCleaner(mesa.Model):

   
    def __init__(self, total_agents, height, width, percent):
        self.num_agents = total_agents
        self.grid = mesa.space.MultiGrid(height, width, True) 
        self.schedule = mesa.time.RandomActivation(self)

        # cSe calcula el tiempo de ejecución
        self.initial_time = time.time()
        self.final_time = 0

        self.celdasSucias = math.ceil((width * height) * percent)
        self.celdasLimpias = math.ceil((width * height) * (1 - percent))

        self.dirty_matrix = [[False for _ in range(height)] for _ in range(width)]

    

        # Se colocan las celdas sucias
        for i in range(self.celdasSucias):

            rand_x = random.randint(0, width-1)
            rand_y = random.randint(0, height-1)
            self.dirty_matrix[rand_x][rand_y] = True




        # Creaación de agentes
        for i in range(total_agents):
            
            # Sumamos el agente a nuestro modelo
            a = AgentCleanerRobot(i, self)

            self.schedule.add(a)

            # Se colocoa a los agentes en la celda incial
            self.grid.place_agent(a, (1, 1))

    def step(self):
        # Imprimir cada step
        self.schedule.step()

    def isDirty(self, new_position):
        x, y = new_position

        # Regresar si en esta posición de la matriz está sucia.
        return self.dirty_matrix[x][y]

    def setDirty(self, new_position):
        # Se determina si la celda esta limpia
        self.celdasSucias = self.celdasSucias - 1
        self.celdasLimpias = self.celdasLimpias + 1

        x, y = new_position

        self.dirty_matrix[x][y] = False

        if self.celdasSucias == 0:
            self.final_time = time.time()  # tiempo de ejecución del programa

    def total_movements(self):
        # iCantidad de moviminetos de los agentes
        return [agent.amount_movements for agent in self.schedule.agents]

    # Porcentaje de celdas limpias
    def dirtyCellRatio(self):
        return self.celdasLimpias / (self.celdasSucias + self.celdasLimpias)

    def program_execution_time(self):
        print('Tiempo de ejecución', self.final_time - self.initial_time, 'segundos')
