import pandas as pd
import os
import os.path as path

from sqlalchemy import column

from src import create_app
from src.models import Paper, create_session, Citation
from sqlalchemy.orm import sessionmaker

def import_papers(csv_path):
    app = create_app()
    with app.app_context():
        session = create_session()
        papers = pd.read_csv(path.join(csv_path, 'papers_predict.csv.gz'), compression='gzip')
        column_name = ['citer', 'citee']
        edges = pd.read_csv(path.join(csv_path, 'edges.csv.gz'), compression='gzip', names=column_name)

        for _, row in papers.iterrows():
            paper = Paper(
                title=row['title'],
                abstract=row['abstract'],
                category=row['category'],
                year=row['year']
            )
            session.add(paper)

        session.commit()

        for _, row in edges.iterrows():
            citation = Citation(
                citer_id=row['citer'] + 1,
                citee_id=row['citee'] + 1
            )
            session.add(citation)

        session.commit()
        session.close()

if __name__ == "__main__":
    import_papers('F:\\grade3_LEARNING\\bigData\\hw3\\LinkedPapers')
