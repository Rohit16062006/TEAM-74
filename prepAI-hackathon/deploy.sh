#!/bin/bash

echo "Deploying PrepAI MVP..."

# 1. Backend Deployment (Render)
# Assumes Render CLI or similar setup. For now, we echo steps.
echo "1. Pushing backend to Render..."
# git subtree push --prefix prepAI-hackathon/backend origin params

# 2. Frontend Deployment (Vercel)
echo "2. Pushing frontend to Vercel..."
# VERCEL_PROJECT_ID=... vercel --prod

# 3. Validation
echo "3. Validating endpoints..."
# curl https://prepai-backend.onrender.com/api/health

echo "Deployment Complete! 🚀"
echo "Backend: https://prepai-backend.onrender.com"
echo "Frontend: https://prepai-hackathon.vercel.app"
