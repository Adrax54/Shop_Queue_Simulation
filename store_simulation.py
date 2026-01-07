import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

"""Input data and simulation variables"""

V_k = 0.5  # half a basket per minute (service speed)

cashier_flag = 1  # number of cashiers serving one checkout

simulation_time = 20  # duration of the simulation (minutes)

"""Simulation initialization"""

env = simpy.RealtimeEnvironment()

# Create checkouts
checkout_line1 = simpy.Resource(env, capacity=cashier_flag)
checkout_line2 = simpy.Resource(env, capacity=cashier_flag)
checkout_line3 = simpy.Resource(env, capacity=cashier_flag)
checkout_line4 = simpy.Resource(env, capacity=cashier_flag)
checkout_line5 = simpy.Resource(env, capacity=cashier_flag)

checkout_lines = []

checkout_lines.append(checkout_line1)
checkout_lines.append(checkout_line2)
checkout_lines.append(checkout_line3)
checkout_lines.append(checkout_line4)
checkout_lines.append(checkout_line5)

times = []

"""The simulation takes place here"""

def QueueSimulation(checkout_lines, env, name, V, cashier_limit):

    global times

    """
    This function simulates a store checkout queue.

    Input parameters:
        checkout_lines - store checkouts (list)
        env - simulation environment (simpy environment)
        name - name of the customer
        V - service speed in baskets per minute
        cashier_limit - number of people in queue that triggers using the next checkout

    Output:
        Simulation flow
        Average time spent by a customer in the system
    """

    # Approaching the checkouts
    yield env.timeout(random.uniform(0.1, 0.5))
    start_time = env.now
    print('%s is looking for a free checkout at time: %d' % (name, env.now))

    # Assign checkouts
    customer_line1 = checkout_lines[0]
    customer_line2 = checkout_lines[1]
    customer_line3 = checkout_lines[2]
    customer_line4 = checkout_lines[3]
    customer_line5 = checkout_lines[4]

    # Calculate queue lengths
    queue_length_1 = len(customer_line1.queue)
    queue_length_2 = len(customer_line2.queue)
    queue_length_3 = len(customer_line3.queue)
    queue_length_4 = len(customer_line4.queue)
    queue_length_5 = len(customer_line5.queue)

    print('Queue at checkout 1:', queue_length_1)
    print('Queue at checkout 2:', queue_length_2)
    print('Queue at checkout 3:', queue_length_3)
    print('Queue at checkout 4:', queue_length_4)
    print('Queue at checkout 5:', queue_length_5)

    # Customer checks checkout 1
    if queue_length_1 < cashier_limit:

        with customer_line1.request() as rq:
            yield rq

            basket_size = random.uniform(0.1, 2)
            checkout_time = basket_size / V

            print('%s starts checkout at checkout 1 at time %d' % (name, env.now))
            yield env.timeout(checkout_time)
            print('%s leaves checkout 1 at time %d' % (name, env.now))
            end_time = env.now

    elif queue_length_1 >= cashier_limit:

        # Checkout 1 busy, go to checkout 2
        if queue_length_2 < cashier_limit:

            with customer_line2.request() as rq1:
                yield rq1

                basket_size = random.uniform(0.1, 2)
                checkout_time = basket_size / V

                print('%s starts checkout at checkout 2 at time %d' % (name, env.now))
                yield env.timeout(checkout_time)
                print('%s leaves checkout 2 at time %d' % (name, env.now))
                end_time = env.now

        elif queue_length_2 >= cashier_limit:

            # Checkout 2 busy, go to checkout 3
            if queue_length_3 < cashier_limit:

                with customer_line3.request() as rq2:
                    yield rq2

                    basket_size = random.uniform(0.1, 2)
                    checkout_time = basket_size / V

                    print('%s starts checkout at checkout 3 at time %d' % (name, env.now))
                    yield env.timeout(checkout_time)
                    print('%s leaves checkout 3 at time %d' % (name, env.now))
                    end_time = env.now

            elif queue_length_3 >= cashier_limit:

                # Checkout 3 busy, go to checkout 4
                if queue_length_4 < cashier_limit:

                    with customer_line4.request() as rq3:
                        yield rq3

                        basket_size = random.uniform(0.1, 2)
                        checkout_time = basket_size / V

                        print('%s starts checkout at checkout 4 at time %d' % (name, env.now))
                        yield env.timeout(checkout_time)
                        print('%s leaves checkout 4 at time %d' % (name, env.now))
                        end_time = env.now

                elif queue_length_4 >= cashier_limit:

                    # Checkout 4 busy, go to checkout 5
                    if queue_length_5 < cashier_limit:

                        with customer_line5.request() as rq4:
                            yield rq4

                            basket_size = random.uniform(0.1, 2)
                            checkout_time = basket_size / V

                            print('%s starts checkout at checkout 5 at time %d' % (name, env.now))
                            yield env.timeout(checkout_time)
                            print('%s leaves checkout 5 at time %d' % (name, env.now))
                            end_time = env.now

                    elif queue_length_5 >= cashier_limit:

                        # Special case: all checkouts are busy
                        # Customer chooses the shortest queue
                        queues = [
                            queue_length_1,
                            queue_length_2,
                            queue_length_3,
                            queue_length_4,
                            queue_length_5
                        ]

                        shortest_queue = min(queues)
                        checkout_id = queues.index(shortest_queue)

                        with checkout_lines[checkout_id].request() as rq5:
                            yield rq5

                            basket_size = random.uniform(0.1, 2)
                            checkout_time = basket_size / V

                            print('%s starts checkout at checkout %d at time %d' %
                                  (name, checkout_id + 1, env.now))
                            yield env.timeout(checkout_time)
                            print('%s leaves checkout %d at time %d' %
                                  (name, checkout_id + 1, env.now))
                            end_time = env.now

    time_spent = end_time - start_time
    times.append(time_spent)
    print('%s spent this much time in the store: %d' % (name, time_spent))


""" RUN """


def next_customer(env):
    """
    This function runs the simulation and
    generates time intervals between arriving customers
    """

    customer_id = 1

    while True:
        yield env.timeout(random.uniform(0.3, 0.9))  # Customers arrive every 0.3–0.9 minutes
        env.process(QueueSimulation(
            checkout_lines,
            env,
            'Customer %d' % customer_id,
            V_k,
            4
        ))
        customer_id += 1


# Start simulation process
env.process(next_customer(env))

# Run simulation
env.run(until=simulation_time)

print("!!! SIMULATION FINISHED !!!")
print("Time list:\n", times, "\n")
print("Average time spent in the system:", np.mean(times))
print("Shortest time spent in the system:", np.min(times))
print("Longest time spent in the system:", np.max(times))

plt.plot(times)
plt.title("Time Spent in Store")
plt.ylabel("Time in Minutes")
plt.xlabel("Customer Number")
plt.show()
