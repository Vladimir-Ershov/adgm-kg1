import os
from neo4j import GraphDatabase
import pickle
import time
import numpy as np
import argparse

GLOBAL_ISSUES = []


def init_args_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description="Script to process graph queries instead of dump")
    parser.add_argument(
        "--input",
        metavar="path",
        required=False,
        default="../data/raw/",
        help="fold where pkl files are located",
    )
    parser.add_argument(
        "--uri",
        metavar=str,
        required=False,
        default="bolt://localhost:7474",
        help="URI to connect to neo4j",
    )
    parser.add_argument(
        "--username",
        metavar=str,
        required=False,
        default="neo4j",
        help="Neo4j db username",
    )
    parser.add_argument(
        "--password",
        metavar=str,
        required=False,
        default="neo4j",
        help="Neo4j db username's password",
    )

    parser.add_argument(
        "--size",
        metavar=int,
        required=False,
        default=64,
        help="Batch size. How many queries will be sent before tx.commit",
    )

    return parser


def main():

    args = init_args_parser().parse_args()
    print("App started")

    input = args.input
    os.makedirs(input, exist_ok=True)

    order = [
        "to_paragraph_nodes_logs.pkl",
        "to_paragraph_connections_log.pkl",
        "to_obligations_occur.pkl",
        "to_obligations_link.pkl",
        "create_doc.pkl"
    ]

    def po(path):
        return os.path.join(input, path)

    driver = (
        GraphDatabase.driver(
            args.uri,
            auth=(args.username, args.password),
        )
    )

    all_data = []
    for fn in order:
        data = pickle.load(open(po(fn), "rb"))
        if len(data) <= 0:
            print(f"Error {fn} is {data}")
        else:
            print(f"in {po(fn)} got {len(data)}")
        all_data.extend(data)

    data_len = len(all_data)
    prc = []
    with driver.session() as session:
        tx = session.begin_transaction()
        print(f"Connection to RDMS is opened {session} for len {data_len}")
        cf = 0
        batch_size = args.size
        for d in all_data:
            tx.run(d)
            cf += 1
            if cf % batch_size == 0:
                fst = time.time()
                tx.commit()
                prc.append(time.time() - fst)
                tx = session.begin_transaction()
                if cf % (batch_size * 10) == 0:
                    print(
                        "{} : {}/{} remaining: {:.2f} minutes for {}".format(
                            str(time.ctime()),
                            cf,
                            data_len,
                            (np.mean(prc) / 60) * (data_len - cf) / batch_size,
                            d,
                            )
                    )
        tx.commit()
    print(f"GOT {len(GLOBAL_ISSUES)}!")
    driver.close()
    if len(GLOBAL_ISSUES) > 0:
        pickle.dump(GLOBAL_ISSUES, open("GLOBAL_ISSUES.pkl", "wb"))

    print("App finished successfully!")


if __name__ == "__main__":
    main()
