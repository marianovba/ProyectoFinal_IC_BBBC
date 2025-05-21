SIMULATION_TIME = 480
MIN_STATE_DURATION = 40
STATES_PER_LIGHT = SIMULATION_TIME // MIN_STATE_DURATION
NUM_TRAFFIC_LIGHTS = 4
GENOTYPE_LENGTH = STATES_PER_LIGHT * NUM_TRAFFIC_LIGHTS

def simulate_traffic(individual, entry_interval=5):
    light_sequences = [
        individual[i * STATES_PER_LIGHT : (i + 1) * STATES_PER_LIGHT]
        for i in range(NUM_TRAFFIC_LIGHTS)
    ]
    vehicle_queues = [[] for _ in range(NUM_TRAFFIC_LIGHTS)]
    total_vehicles = 0
    total_exited = 0
    total_wait_time = 0
    max_wait_time = 0

    for t in range(SIMULATION_TIME):
        if t % entry_interval == 0:
            for q in vehicle_queues:
                q.append(t)
                total_vehicles += 1

        state_idx = t // MIN_STATE_DURATION
        for i, queue in enumerate(vehicle_queues):
            if light_sequences[i][state_idx] == 1 and queue:
                enter_time = queue.pop(0)
                wait_time = t - enter_time
                total_wait_time += wait_time
                max_wait_time = max(max_wait_time, wait_time)
                total_exited += 1

    return {
        "total_in": total_vehicles,
        "total_out": total_exited,
        "total_wait_time": total_wait_time,
        "max_wait_time": max_wait_time
    }
