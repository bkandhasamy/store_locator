from locust import HttpUser, task, between


class APILoadTest(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks

    @task(1)
    def get_all_locations(self):
        self.client.get("http://0.0.0.0:8000/locations")

    @task(2)
    def get_single_location(self):
        self.client.get("http://0.0.0.0:8000/locations/1")

    @task(1)
    def create_location(self):
        self.client.post(
            "http://0.0.0.0:8000/locations",
            json={
                "latitude": 51.1942536,
                "longitude": 6.455508,
                "availability_radius": 5,
                "open_hour": "14:00:00",
                "close_hour": "23:00:00",
                "rating": 4.7,
            },
        )

    @task(1)
    def get_stores_for_location(self):
        self.client.get("http://0.0.0.0:8000/locations/coordinates/51.1942536%7C6.455508")
