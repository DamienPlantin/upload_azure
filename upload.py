import argparse
import configparser
import logging
import os
import os.path
import sys
from azure.storage.blob import BlobServiceClient


conteneur = os.environ['conteneur']
stockage = os.environ['stockage']
path = "C:/Users/Damien/Desktop/Simplon/Git/Azure_storage/Dossier_upload/"
All = os.listdir(path)


def main(config):
    """
    Cette fonction est lancé au démarrage du script
    Fais le liens avec le fichier config.ini
    En fonction de l'argument, appel la fonction associée
    """
    cible = input("Nom du livre : ")
    blobclient = BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    containerclient = blobclient.get_container_client(
        conteneur)
    logging.info(f"Valeur de l'input : {cible}")
    if cible == "All":
        for livre in All:
            livre = path+livre
            blobclient = containerclient.get_blob_client(
                    os.path.basename(livre))
            logging.debug(f"Compte {stockage}")
            logging.debug(f"Conteneur {conteneur}")
            logging.info("Connexion réussie")
            with open(livre, "rb") as f:
                logging.info(f"Upload du fichier {livre} vers le conteneur")
                logging.warning(
                    f"Ecrasement du fichier {livre}")
                blobclient.upload_blob(f, overwrite=True)
    else:
        cible = path+cible
        blobclient = containerclient.get_blob_client(os.path.basename(cible))
        logging.debug(f"Compte {stockage}")
        logging.debug(f"Conteneur {conteneur}")
        logging.info("Connexion réussie")
        with open(cible, "rb") as f:
            logging.info(f"Upload du fichier {cible} vers le conteneur")
            logging.warning(
                f"Ecrasement du fichier {cible} s'il existe dans le conteneur")
            blobclient.upload_blob(f, overwrite=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument(
        "-cfg",
        default="config.ini",
        help="chemin du fichier de configuration")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(config))
