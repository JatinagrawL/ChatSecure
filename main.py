from app import app

# Vercel requires the app to be available as a variable
# This ensures compatibility with Vercel's serverless functions
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Export app for Vercel deployment
application = app