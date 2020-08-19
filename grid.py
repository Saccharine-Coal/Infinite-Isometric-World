import random

from settings import *

class Grid:
    def __init__(self, object_type):
        self.length = CHUNKSIZE
        self.chunk_num = CHUNKS
        self.width = self.length * TILEWIDTH * CHUNKS *100
        self.height = self.length * TILEHEIGHT * CHUNKS
        self.rect_l = RENDERDISTANCE * self.length
        self.max_x = self.max_y = CHUNKS * CHUNKSIZE
        self.min_x = self.min_y = 0
        self.obj = object_type
        self.obj_dict = {}

    def init_chunks(self):
        """Creates the chunks and stores them in a dictionary.
            Each key is the first tile in the chunk list."""
        chunks = {}
        for chunk_x in range(self.chunk_num):
            for chunk_y in range(self.chunk_num):
                # Create a dictionary entry of a length x length sized nested list of tiles.
                chunks[(chunk_x*self.length, chunk_y*self.length)] = [
                [random.choice([None, 1, 2, 3, 4]) for chunk_length_x in range(self.length)]
                    for chunk_length_y in range(self.length)]
        # Save the chunk dictionary.
        self.chunks = chunks
        # Save a list of the keys that can be iterated through.
        self.key_list = [*chunks]
        print(self.key_list)

    def init_objects(self):
        """Hack solution to create enough tile objects for the grid."""
        for i in range(1, 5):
            self.obj_dict[i] = self.obj(i)

    def render_chunks(self, x, y):
        """Function that checks the proximity of the player to render chunks
            appropriately as the player moves through the grid."""
        temp_list = []
        a, b, c, d = x + self.rect_l, y + self.rect_l, x - self.rect_l, y - self.rect_l
        for i in range(len(self.key_list)):
            key = self.key_list[i]
            if key[0]<=a and key[0]>=c:
                if key[1]<=b and key[1]>=d:
                    temp_list.append(
                            self._iterate_chunk(key[0], key[1], self.chunks[(key[0], key[1])]
                            ))
                    self._check_to_gen(key[0], key[1])
        return temp_list

    def _check_to_gen(self, chunk_x, chunk_y):
        """Checks every possible chunk to generate."""
        # Postive x, y
        if self.chunks.get((chunk_x+self.length, chunk_y)) is None:
            self._generate_chunk(chunk_x+self.length, chunk_y)
            self.max_x += self.length
        if self.chunks.get((chunk_x, chunk_y+self.length)) is None:
            self._generate_chunk(chunk_x, chunk_y+self.length)
            self.max_y += self.length
        if self.chunks.get((chunk_x+self.length, chunk_y+self.length)) is None:
            self._generate_chunk(chunk_x+self.length, chunk_y+self.length)
            self.max_x += self.length
            self.max_y += self.length
        # Negative x, y
        if self.chunks.get((chunk_x-self.length, chunk_y)) is None:
            self._generate_chunk(chunk_x-self.length, chunk_y)
            self.min_x -= self.length
        if self.chunks.get((chunk_x, chunk_y-self.length)) is None:
            self._generate_chunk(chunk_x, chunk_y-self.length)
            self.min_y -= self.length
        if self.chunks.get((chunk_x-self.length, chunk_y-self.length)) is None:
            self._generate_chunk(chunk_x-self.length, chunk_y-self.length)
            self.min_x -= self.length
            self.min_y -= self.length

    def _generate_chunk(self, new_x=0, new_y=0):
        """Generates a chunk at the specified position and adds it to the dictionary."""
        new_key = (new_x, new_y)
        self.chunks[new_key] = [
                [random.choice([None, 1, 2, 3, 4]) for chunk_length_x in range(self.length)]
                for chunk_length_y in range(self.length)]
        self.key_list.append(new_key)
        print(f'''Chunk ({new_x}, {new_y}) generated!''')

    def _iterate_chunk(self, chunk_x, chunk_y, chunk):
        """Helper function to iterate through a chunk."""
        temp_list = []
        for x, row in enumerate(chunk):
            for y, data in enumerate(row):
                if data:
                    temp_list.append(self._check_data(x+chunk_x, y+chunk_y, data))
        return temp_list

    def _check_data(self, x, y, data):
        """Assigns an image and rect to be drawn by pygame for each data."""
        try:
            obj = self.obj_dict[data]
            return obj.image, obj.rect.move((self._convert_cart(x, y)))
        except KeyError:
            print(f'''This data number caused the error: {data}''')

    def _convert_cart(self, x, y):
        """Converts cartesian coordinates to isometric coordinates."""
        cart_x = x * TILEHEIGHT_HALF
        cart_y = y * TILEWIDTH_HALF
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        return iso_x, iso_y
