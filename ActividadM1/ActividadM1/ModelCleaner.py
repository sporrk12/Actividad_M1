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

        # checar si ya esta limpio todo para evitar dar más steps
        if self.model.dirtyCellRatio() >= 0.99:
            self.model.final_time = time.time()
        else:

            self.move()
            self.clean()



            # hay que ir trackeando la cantidad de movimientos para cada agente.
            self.amount_movements = self.amount_movements + 1



class ModelCleaner(mesa.Model):

    # M y N son dimensiones de la habitación
    def __init__(self, total_agents, height, width, percent):

        # poblamos atributos miembros de la clase padre mesa.Model
        self.num_agents = total_agents
        # queremos que sea multigrid el espacio porque varios agentes pueden estar sobre una misma celda.
        self.grid = mesa.space.MultiGrid(height, width, True) # el True es una celda toroidal (las celdas no te sacan)
        self.schedule = mesa.time.RandomActivation(self)

        # calcular tiempo de ejecucion del programa
        self.initial_time = time.time()
        self.final_time = 0

        self.celdasSucias = math.ceil((width * height) * percent)
        self.celdasLimpias = math.ceil((width * height) * (1 - percent))

        # SÍ DEBE SER UN PORCENTAJE. La matriz va a ser una estructura de datos aparte.
        self.dirty_matrix = [[False for _ in range(height)] for _ in range(width)]

        # False -> celda NO sucia (limpia)
        # True -> celda sucia.

        # colocar celdas sucias
        for i in range(self.celdasSucias):

            rand_x = random.randint(0, width-1)
            rand_y = random.randint(0, height-1)
            self.dirty_matrix[rand_x][rand_y] = True




        # crear agentes
        for i in range(total_agents):
            # agregamos un id unico al agente y lo sumamos a nuestro modelo (self)
            a = AgentCleanerRobot(i, self)

            self.schedule.add(a)

            # colocamos a los agentes en la celda [0,0] de la matriz
            self.grid.place_agent(a, (1, 1))

    def step(self):
        # imprimimos para ir registrando en que tiempo vamos.
        self.schedule.step()

    def isDirty(self, new_position):
        x, y = new_position

        # retornar si en esta posicion de la matriz está sucio.
        return self.dirty_matrix[x][y]

    def setDirty(self, new_position):
        # establecemos a verdadero el valor de la matriz en la posición para decir que está limpio.
        self.celdasSucias = self.celdasSucias - 1
        self.celdasLimpias = self.celdasLimpias + 1

        x, y = new_position

        self.dirty_matrix[x][y] = False

        if self.celdasSucias == 0:
            self.final_time = time.time()  # tiempo de ejecución del programa

    def total_movements(self):
        # imprimir la cantidad de movimientos de todos los agentes
        return [agent.amount_movements for agent in self.schedule.agents]

    # nos da el porcentaje de celdas limpias
    def dirtyCellRatio(self):
        return self.celdasLimpias / (self.celdasSucias + self.celdasLimpias)

    def program_execution_time(self):
        print('tiempo de ejecucion', self.final_time - self.initial_time, 'segundos')