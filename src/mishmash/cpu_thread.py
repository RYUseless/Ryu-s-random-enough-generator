import random
import time
import multiprocessing
from pynput.mouse import Controller
from decimal import Decimal


class ThreadExperiment:
    def __init__(self):
        self.dummy = "I AM DUMMY"

    @staticmethod
    def get_rand_mouse():
        x = 1055373 * 73  # VLÁKNO FREKVENCA * poslední dvě čísla
        y1 = 1845911 * 685 * 431314  # prvá část výsledku z cat /proc/stat | grep "cpu7" -- 7 je id
        y2 = 13189725 * 136186 * 82482 * 52843  # druhá část z cat atd.
        mouse = Controller()# poměrně přímočaré, co to je :)
        position = mouse.position
        a = int(position[0])
        b = int(position[1])
        random_num = (a ** b % y2)**3 * (y1 * x) ** 3

        return random_num

    @staticmethod
    def adjust_to_random_num(random_num):
        # získání kurzoru myši na obrazovce
        mouse = Controller()
        position = mouse.position

        # Vybere se jedna z pozic cursoru, zde je možné a vhodné využít random.choice (přece jen jsou jen dvě možnosti)
        random_choice = random.choice([0, 1])
        cursor_value = position[random_choice]

        # Nastavení možné odchylky vygenerovaného čísla od random_num proměnné, ke které je potřeba se dostat
        # Momentálně 0.1% odchylka z obou směrů-- 0.999 a 1.001
        lower_limit = random_num * 0.999
        upper_limit = random_num * 1.001

        # Cyklus, který upravuje náhodně generované číslo, dokud není v požadovaném rozsahu
        attempts = 0
        while not (lower_limit < cursor_value < upper_limit):
            # Pokud je pozice kurzoru menší než random_num, zkusíme ji zvětšit
            if cursor_value < random_num:
                cursor_value *= random.uniform(1.01, 1.1)  # Násobení
            else:
                cursor_value /= random.uniform(1.01, 1.1)  # Dělení

            attempts += 1

        return cursor_value, attempts  # Vracíme upravenou hodnotu a počet pokusů

    def thread_task(self, task_id, results, summary):
        start_time = time.time()

        random_num = self.get_rand_mouse()
        final_value, attempts = self.adjust_to_random_num(random_num)

        end_time = time.time()
        duration = end_time - start_time
        results.append((task_id, duration))  # Ukládáme task_id a čas
        summary.append((task_id, random_num, final_value, attempts, duration))  # Přidáváme čas i do summary

    def run(self):
        print("Thread completion randomness testing")

        # Basically to vezme momentální počet vláken, které lze využít.
        cpu_count = multiprocessing.cpu_count()
        print(f"Number of CPUs: {cpu_count}")

        # Shared list for storing results
        manager = multiprocessing.Manager()
        results = manager.list()  # pouze summary času + pořadí v jakém doběhly tasky -- deprecated kinda now
        summary = manager.list()  # summary doběhlého tasku -- random_num, uhádlé, validní číslo, pokusy a čas

        # Create and start processes
        processes = []
        for i in range(cpu_count):
            process = multiprocessing.Process(target=self.thread_task, args=(i, results, summary))
            processes.append(process)
            process.start()

        # Waiting for all the processes to finish -- sync and join
        for process in processes:
            process.join()

        # sort by completion time
        sorted_results = sorted(results, key=lambda x: x[1])

        # Print the order in which threads finished:
        print("Order of thread completion:")
        for task_id, duration in sorted_results:
            print(f"Thread {task_id} completed in {duration:.4f} seconds")

        # sort by completion time
        sorted_summary = sorted(summary, key=lambda x: x[4])

        # Rand. num. guess output summary:
        print("\nSummary of tasks in order of thread completion:")
        for task_id, random_num, final_value, attempts, duration in sorted_summary:
            print(
                f"Task {task_id} - Random number: {random_num}, Final value: {final_value}, Attempts: {attempts}, Duration: {duration:.4f} seconds")
