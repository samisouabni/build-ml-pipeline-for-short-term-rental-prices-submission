#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ####################
    
    logger.info("Reading data into dataframe")
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    logger.info(f"Dropping outliers on price between {args.min_price} and {args.max_price}")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    logger.info("Convert last_review from str to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    logger.info("Output cleaned data to csv")
    df.to_csv("clean_sample.csv", index=False)
    
    logger.info("Create artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    
    logger.info("Log artifact")
    run.log_artifact(artifact)
    
    logger.info("Finish run")
    run.finish()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The data artifact to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The cleaned data artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The type of data",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="The description of the data",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="The minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="The maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)