import uuid
import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.api.forms import *
from app.api.utils import ApiError
from models import dbsession as conn, BluePrintTerms, BluePrintMethod, DeployManifest, DeployManifestArgs, BluePrint
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_blueprint(req: BlurPrintForm):
    try:
        # Create a new BluePrint instance using the validated data
        new_blueprint = BluePrint(
            slug=req.slug,
            description=req.description,
            price=req.price,
            package_addr=req.package_address
        )

        # Add terms if provided
        if req.terms:
            for term in req.terms:
                new_term = BluePrintTerms(
                    blueprint_slug=req.slug,
                    term=term.term,
                    description=term.description
                )
                new_blueprint.terms.append(new_term)

        if req.deploy_manifest:
            manifest = DeployManifest(
                manifest=req.deploy_manifest.mainfest,
                blueprint_slug=req.slug
            )
            manifest_args = []
            for args in req.deploy_manifest.manifest_args:
                arg = DeployManifestArgs(
                    key=args.key,
                    type=str(args.value)
                )
                manifest_args.append(arg)
            manifest.deploymanifestargs = manifest_args

        new_blueprint.deploy_mainfest = manifest

        # Add the new blueprint to the conn and commit
        conn.add(new_blueprint)
        conn.commit()
        logger.info(f"Successfully added new blueprint: {new_blueprint.slug}")
        return new_blueprint

    except IntegrityError as e:
        conn.rollback()
        logger.error(f"Integrity error occurred: {e}")
        raise HTTPException(status_code=400,
                            detail="Integrity error: possibly duplicate entry or foreign key constraint.")

    except SQLAlchemyError as e:
        conn.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        conn.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_blueprint_deploymanifest(slug: str):
    try:
        stmt = (select(BluePrint, DeployManifest, DeployManifestArgs).join(DeployManifest,
                                                                                               BluePrint.slug == DeployManifest.blueprint_slug).join(
            DeployManifestArgs, DeployManifestArgs.blueprint_slug == DeployManifest.blueprint_slug)).where(
            BluePrint.slug == slug)

        blueprint, manifest, args = conn.execute(stmt).first()

        return {
            'blueprint': blueprint,
            'manifest': manifest,
            'agrs': args
        }
    except SQLAlchemyError as e:
        conn.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        conn.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_blueprints():
    try:
        blueprint = conn.query(BluePrint).join(BluePrintTerms, BluePrint.slug == BluePrintTerms.blueprint_slug).all()
        if blueprint is None:
            return {}
        return blueprint
    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Function to get a blueprint by slug
def get_blueprint_detail(slug: str):
    try:
        bp = conn.query(BluePrint).options(joinedload(BluePrint.terms)).options(joinedload(BluePrint.deploy_mainfest)).filter(BluePrint.slug == slug ).first()
        return bp
    except SQLAlchemyError as e:
        # Log the error e
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
