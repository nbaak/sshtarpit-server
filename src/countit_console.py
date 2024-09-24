from countit_adapter import get_countit_client


def purge_metrics(countit):
    countit.delete("connections")
    countit.delete("connections_per_ip")
    countit.delete("connections_duration")
    countit.delete("connections_per_country")
    countit.delete("test_counter")
    
    
def main():
    countit = get_countit_client()
    metrics = countit.metrics()
    # purge_metrics(countit)
    
    print("CONSOLE")
    for metric in metrics:
        if metric == "test_counter": continue
        print(f"{metric}")
        data = countit.data(metric)
        
        # print sorted by value
        for label, value in sorted(data, key=lambda x: x[1], reverse=True):
            if label == "__default_label__": continue
            print(value, label)
        
        print()

    
if __name__ == "__main__":
    main()
