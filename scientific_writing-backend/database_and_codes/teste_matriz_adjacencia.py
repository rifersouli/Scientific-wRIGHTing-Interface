import time

class Graph(object):

    # Initialize the matrix
    def __init__(self, size):
        self.adjMatrix = []
        for i in range(size):
            self.adjMatrix.append([0 for i in range(size)])
        self.size = size

    # Add edges
    def add_edge(self, v1, v2):
        if v1 == v2:
            print(f'Same vertex {v1} and {v2}')
        self.adjMatrix[v1][v2] = 1
        self.adjMatrix[v2][v1] = 1

    # Remove edges
    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            print(f'No edge between {v1} and {v2}')
            return
        self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v2][v1] = 0

    def __len__(self):
        return self.size

    # Print the matrix
    def print_matrix(self):
        for row in self.adjMatrix:
            for val in row:
                print(f'{val}')
                print(f'{row}')


def main():
    g = Graph(100)
    for i in range(0,99):
        g.add_edge(i, i+1)

    g.print_matrix()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
