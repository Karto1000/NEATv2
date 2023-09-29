import pygame

from Client import Client
from Config import Config
from NEAT import NEAT

pygame.init()
pygame.display.set_caption("NEAT - Neural Network")
SCREEN = pygame.display.set_mode((Config.SW, Config.SH))
FONT = pygame.font.Font(pygame.font.get_default_font(), 14)
current_client = 0

neat = NEAT(Config.NETWORK_STRUCTURE)
clients = [Client(neat, Config.NETWORK_STRUCTURE) for i in range(Config.AMOUNT_OF_CLIENTS)]
neat.set_clients(clients)

while True:
    SCREEN.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if current_client >= Config.AMOUNT_OF_CLIENTS - 1:
                    current_client = 0
                else:
                    current_client += 1
            if event.key == pygame.K_LEFT:
                if current_client <= 0:
                    current_client = Config.AMOUNT_OF_CLIENTS - 1
                else:
                    current_client -= 1
            if event.key == pygame.K_p:
                pass
            if event.key == pygame.K_n:
                try:
                    clients[current_client].add_random_node()
                except Exception as e:
                    print(e)
            if event.key == pygame.K_c:
                try:
                    clients[current_client].add_random_connection()
                except Exception as e:
                    print(e)
            if event.key == pygame.K_g:
                neat.next_generation()

    text = FONT.render(f"Current Genome {current_client + 1}", True, (74, 246, 38))
    SCREEN.blit(text, (10, 10))

    genome = clients[current_client].genome
    for node in genome.nodes.list:
        pygame.draw.circle(
            SCREEN,
            (74, 246, 38),
            (node.x * 500 + Config.NETWORK_PADDING, node.y * 500 + Config.NETWORK_PADDING),
            5
        )

    for connection in genome.connections.list:
        pygame.draw.line(
            SCREEN,
            (74, 246, 38),
            (connection.from_node.x * 500 + Config.NETWORK_PADDING,
             connection.from_node.y * 500 + Config.NETWORK_PADDING),
            (connection.to_node.x * 500 + Config.NETWORK_PADDING, connection.to_node.y * 500 + Config.NETWORK_PADDING)
        )

    pygame.display.flip()
