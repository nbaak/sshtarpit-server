
import argparse
from countit_adapter import get_countit_client


def purge_metrics(countit):
    countit.add_metric("connections_session", overwrite=True)
    countit.add_metric("connections_per_ip", overwrite=True)
    countit.add_metric("connections_duration", overwrite=True)
    countit.add_metric("connections_per_country", overwrite=True)
    countit.delete("test_counter")
    
    
def main(show_count:int=10, show_default=False, purge_first:bool=False):
    countit = get_countit_client()
    metrics = countit.metrics()
    
    if purge_first:
        purge_metrics(countit)
        print("Database purged!")
    
    static_subtraction = 1 if not show_default else 0
    
    print("CONSOLE")
    for metric in metrics:
        if metric == "test_counter": continue
        data = countit.data(metric)
        data_len = len(data) - static_subtraction if len(data) > 0 else 0
        print(f"{metric} ({data_len})")
        
        # print sorted by value
        for label, value in sorted(data, key=lambda x: x[1], reverse=True)[:show_count]:
            if label == "__default_label__" and not show_default: continue
            print(value, label)
        
        print()
        
        
def cli(): 
    parser = argparse.ArgumentParser(description="Tarpit Console")
    parser.add_argument("--show-count", "-sc", help=f"Show N entries per section, default 10", default=10, type=int, action="store")
    parser.add_argument("--show-default", help="Show default section, default False", action="store_true")
    parser.add_argument("--purge-database", help="Empty all Metrics", action="store_true")
    
    args = parser.parse_args()
    
    main(args.show_count, args.show_default, args.purge_database)

    
if __name__ == "__main__":
    cli()
