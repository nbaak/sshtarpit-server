from countit_adapter import get_countit_client


def purge_metrics(countit):
    countit.delete("connections_per_ip")
    countit.delete("connections_duration")
    countit.delete("connections_per_country")
    countit.delete("test_counter")
    
    
def main(show_count:int=10, dont_show_default=True):
    countit = get_countit_client()
    metrics = countit.metrics()
    # purge_metrics(countit)
    
    static_subtraction = 1 if dont_show_default else 0
    
    print("CONSOLE")
    for metric in metrics:
        if metric == "test_counter": continue
        data = countit.data(metric)
        print(f"{metric} ({len(data)-static_subtraction})")
        
        # print sorted by value
        for label, value in sorted(data, key=lambda x: x[1], reverse=True)[:show_count]:
            if label == "__default_label__": continue
            print(value, label)
        
        print()

    
if __name__ == "__main__":
    main()
