from countit_adapter import initialize


def main():
    countit = initialize()
    metrics = countit.metrics()
    
    print("CONSOLE")
    for metric in metrics:
        print(f"{metric}")
        labels = countit.labels(metric)
        for label in labels:
            values = countit.get(metric, label=label)
            print(values, label)
    
    
if __name__ == "__main__":
    main()