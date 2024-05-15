from diablo2_mod_sql.data.table import DataColumnCollection, DataColumnType

txt_columns_map = {
    'actinfo.txt': DataColumnCollection([
        {'name': 'act', 'type': DataColumnType.INTEGER},
        {'name': 'town', 'type': DataColumnType.STRING},
        {'name': 'start', 'type': DataColumnType.STRING},
        {'name': 'maxnpcitemlevel', 'type': DataColumnType.INTEGER},
        {'name': 'classlevelrangestart', 'type': DataColumnType.STRING},
        {'name': 'classlevelrangeend', 'type': DataColumnType.STRING},
        {'name': 'wanderingnpcstart', 'type': DataColumnType.INTEGER},
        {'name': 'wanderingnpcrange', 'type': DataColumnType.INTEGER},
        {'name': 'commonactcof', 'type': DataColumnType.STRING},
        {'name': 'waypoint1', 'type': DataColumnType.STRING},
        {'name': 'waypoint2', 'type': DataColumnType.STRING},
        {'name': 'waypoint3', 'type': DataColumnType.STRING},
        {'name': 'waypoint4', 'type': DataColumnType.STRING},
        {'name': 'waypoint5', 'type': DataColumnType.STRING},
        {'name': 'waypoint6', 'type': DataColumnType.STRING},
        {'name': 'waypoint7', 'type': DataColumnType.STRING},
        {'name': 'waypoint8', 'type': DataColumnType.STRING},
        {'name': 'waypoint9', 'type': DataColumnType.STRING},
        {'name': 'wanderingMonsterPopulateChance', 'type': DataColumnType.INTEGER},
        {'name': 'wanderingMonsterRegionTotal', 'type': DataColumnType.INTEGER},
        {'name': 'wanderingPopulateRandomChance', 'type': DataColumnType.INTEGER},
    ]),
}
