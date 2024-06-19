import time

class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0.0

    def update(self):
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time > 1.0:  # calculate FPS every second
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = current_time


# Example usage:
if __name__ == "__main__":
    fps_counter = FPSCounter()

    while True:
        # Simulate some processing time (replace with actual processing)
        time.sleep(0.1)

        # Update FPS counter
        fps_counter.update()

    
        print(f"Current FPS: {fps_counter.fps:.2f}")
