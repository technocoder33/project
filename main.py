import csv


class RouteMap:
    places = {
        "A": "Place A",
        "B": "Place B",
        "C": "Place C",
        "D": "Place D",
        "E": "Place E",
        "F": "Place F",
    }

    def __init__(self):
        self.paths = {}
        for place in self.places:
            self.paths[place] = {}

        with open("paths.csv", newline="") as file:
            for row in csv.DictReader(file):
                start = row["start"]
                end = row["end"]
                path = {
                    "distance_m": float(row["distance_m"]),
                    "shade_pct": float(row["shade_pct"]),
                    "heat_index": float(row["heat_index"]),
                }
                self.paths[start][end] = path
                self.paths[end][start] = path


class RoutePlanner:
    def __init__(self, route_map):
        self.route_map = route_map

    def heat_score(self, path):
        minutes = path["distance_m"] / 80
        heat_factor = path["heat_index"] / 30
        direct_sun = 1 + 1.0 * (1 - path["shade_pct"] / 100)
        return minutes * heat_factor * direct_sun

    def find_route(self, start, end, cost_type):
        best = {}
        for place in self.route_map.places:
            best[place] = float("inf")
        best[start] = 0
        previous = {}
        unvisited = set(self.route_map.places)

        while unvisited:
            current = None
            for place in self.route_map.places:
                if place in unvisited:
                    if current is None or best[place] < best[current]:
                        current = place

            if best[current] == float("inf") or current == end:
                break

            unvisited.remove(current)
            for neighbor in self.route_map.paths[current]:
                if neighbor in unvisited:
                    path = self.route_map.paths[current][neighbor]
                    if cost_type == "distance":
                        step_cost = path["distance_m"]
                    else:
                        step_cost = self.heat_score(path)
                    new_cost = best[current] + step_cost
                    if new_cost < best[neighbor]:
                        best[neighbor] = new_cost
                        previous[neighbor] = current

        if best[end] == float("inf"):
            return None

        places = [end]
        distance = 0
        heat = 0
        place = end
        while place != start:
            prior = previous[place]
            path = self.route_map.paths[prior][place]
            distance += path["distance_m"]
            heat += self.heat_score(path)
            places.append(prior)
            place = prior
        places.reverse()
        return {"places": places, "distance_m": distance, "heat_score": heat}


def ask_location(label):
    while True:
        answer = input(label + " (A-F, Q to quit): ").strip().upper()
        if answer == "Q":
            return None
        if answer in RouteMap.places:
            return answer
        print("Invalid location. Enter A, B, C, D, E, or F.")


def show_route(label, route):
    print(label + ": " + " -> ".join(route["places"]))
    print("Distance: {:g} m".format(route["distance_m"]))
    print("Time: {:.1f} min".format(route["distance_m"] / 80))
    print("Heat score: {:.2f}".format(route["heat_score"]))


def main():
    route_map = RouteMap()
    planner = RoutePlanner(route_map)
    print("Pathfinder")

    while True:
        print("\nLocations:")
        for code in route_map.places:
            print(code + ": " + route_map.places[code])

        start = ask_location("Start")
        if start is None:
            break
        end = ask_location("Destination")
        if end is None:
            break

        shortest = planner.find_route(start, end, "distance")
        cooler = planner.find_route(start, end, "heat")
        print()
        if shortest is None:
            print("Route: No route from " + start + " to " + end)
        else:
            show_route("Shortest route", shortest)
            print()
            show_route("Cooler route", cooler)

            if shortest["places"] != cooler["places"]:
                extra_time = (cooler["distance_m"] - shortest["distance_m"]) / 80
                reduction = (
                    100
                    * (shortest["heat_score"] - cooler["heat_score"])
                    / shortest["heat_score"]
                )
                print("\nExtra time: {:.1f} min".format(extra_time))
                print("Heat reduction: {:.1f}%".format(reduction))

        while True:
            again = input("\nSearch another route? (Y/N, Q to quit): ").strip().upper()
            if again == "Y" or again == "N" or again == "Q":
                break
            print("Enter Y, N, or Q.")
        if again != "Y":
            break

    print("Goodbye.")


main()
