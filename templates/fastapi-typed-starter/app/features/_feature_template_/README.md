# Feature Template

Copy this folder when adding a new feature.

1. Rename `_feature_template_` to the feature name, for example `projects`.
2. Update imports from `app.features._feature_template_` to the new module.
3. Add feature schemas in `schemas.py`.
4. Keep business logic in `service.py`.
5. Expose HTTP routes from `router.py`.
6. Mount the feature router in `app/api/router.py`.

This mirrors the Create-Node-App `_feature-template_` pattern while using a
Python-safe package name.
