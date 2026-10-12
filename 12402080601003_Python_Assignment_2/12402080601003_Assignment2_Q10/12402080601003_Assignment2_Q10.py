# Assignment 2
# Question 10 - Python Data Visualization Dashboard Exporter

import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    file_path = input("CSV file path: ").strip()
    output_folder = input("Output folder: ").strip()

    try:
        os.makedirs(output_folder, exist_ok=True)

        df = pd.read_csv(file_path)

        if "enrollment" not in df.columns or "name" not in df.columns:
            print("INVALID")
            return

        subjects = [
            col for col in df.columns
            if col not in ["enrollment", "name"]
        ]

        if not subjects:
            print("INVALID")
            return

        for subject in subjects:
            df[subject] = pd.to_numeric(
                df[subject], errors="coerce"
            )
            df.loc[~df[subject].between(0, 100), subject] = float("nan")
            df[subject] = df[subject].fillna(df[subject].mean())
            df[subject] = df[subject].fillna(0)

        df.to_csv(
            os.path.join(output_folder, "cleaned_marks.csv"),
            index=False
        )

        summary = df[subjects].agg(["mean", "min", "max"]).T
        summary.columns = ["average", "minimum", "maximum"]
        summary.to_csv(
            os.path.join(output_folder, "summary.csv")
        )

        grades = df[subjects].stack()
        plt.figure()
        grades.plot(kind="hist", bins=10, edgecolor="black")
        plt.title("Grade Distribution")
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(
            os.path.join(output_folder, "grade_distribution.png")
        )
        plt.close()

        summary["average"].plot(kind="bar")
        plt.title("Subject-wise Average")
        plt.ylabel("Average Marks")
        plt.tight_layout()
        plt.savefig(
            os.path.join(output_folder, "subject_average.png")
        )
        plt.close()

        df["total"] = df[subjects].sum(axis=1)
        top = df.nlargest(min(10, len(df)), "total")

        plt.figure()
        plt.bar(top["name"].astype(str), top["total"])
        plt.title("Top Performers")
        plt.xlabel("Student")
        plt.ylabel("Total Marks")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(
            os.path.join(output_folder, "top_performers.png")
        )
        plt.close()

        print("Files created:")
        print("cleaned_marks.csv")
        print("summary.csv")
        print("grade_distribution.png")
        print("subject_average.png")
        print("top_performers.png")

    except (OSError, ValueError, pd.errors.ParserError):
        print("INVALID")


if __name__ == "__main__":
    main()