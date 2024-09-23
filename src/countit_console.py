from countit_adapter import initialize


def purge_metrics(countit):
    countit.delete("connections")
    countit.delete("connections_per_ip")
    countit.delete("connections_duration")


def main():
    countit = initialize()
    metrics = countit.metrics()
    # purge_metrics(countit)
    
    print("CONSOLE")
    for metric in metrics:
        print(f"{metric}")
        labels = countit.labels(metric)
        for label in labels:
            if label == "__default_label__": continue
            values = countit.get(metric, label=label)
            print(values, label)
        print()
        

    
if __name__ == "__main__":
    main()
