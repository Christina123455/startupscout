# 🚀 Deployment Guide - Startup Scout

**Time required: 15 minutes**  
**Cost: $0/month**  
**Difficulty: Easy** (just clicking buttons!)

---

## 📋 What You'll Need

✅ GitHub account (free)  
✅ That's it!

---

## 🎯 Deployment Steps

### **STEP 1: Create Vercel Account** (2 minutes)

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel
5. ✅ Done!

**What is Vercel?**  
Free hosting for your frontend. 100GB bandwidth/month (plenty for 1000+ users).

---

### **STEP 2: Create Supabase Account** (3 minutes)

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Choose "Continue with GitHub"
4. Click "New Project"
5. Fill in:
   - **Name:** `startup-scout`
   - **Database Password:** (choose a strong password, save it!)
   - **Region:** Choose closest to you (e.g., "London")
6. Click "Create new project"
7. **Wait 2 minutes** while project initializes ⏳

**What is Supabase?**  
Free PostgreSQL database + authentication. 500MB storage (plenty for jobs data).

---

### **STEP 3: Get Supabase Credentials** (1 minute)

**While your Supabase project is initializing:**

1. Once ready, click "Settings" (gear icon in sidebar)
2. Click "API" in the settings menu
3. You'll see two important values:

**Copy these - you'll need them:**

```
Project URL: https://xxxxx.supabase.co
API Key (anon, public): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Save these somewhere safe!** (You'll paste them in Step 5)

---

### **STEP 4: Fork & Deploy** (3 minutes)

1. **Fork this repository:**
   - Click "Fork" button at top right of this GitHub page
   - Click "Create fork"

2. **Deploy to Vercel:**
   - Click the button below:

   [![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/startup-scout)

3. **Configure deployment:**
   - Vercel will ask for your GitHub repo → Select the fork you just created
   - It will ask for environment variables → Click "Add"

4. **Add environment variables:**
   ```
   NEXT_PUBLIC_SUPABASE_URL = (paste your Supabase Project URL)
   NEXT_PUBLIC_SUPABASE_ANON_KEY = (paste your Supabase API Key)
   ```

5. **Click "Deploy"**
6. **Wait 2 minutes** for deployment ⏳
7. ✅ Your site is live!

**Your URL:** `startup-scout-xxxxx.vercel.app`

---

### **STEP 5: Initialize Database** (2 minutes)

**Now set up your database tables:**

1. Go back to Supabase dashboard
2. Click "SQL Editor" in sidebar
3. Click "New query"
4. **Copy the entire contents** of `database/schema.sql` file
5. **Paste into the editor**
6. Click "Run" (or press Cmd/Ctrl + Enter)
7. You should see "Success. No rows returned"
8. ✅ Database is ready!

**What did this do?**  
Created all tables (users, jobs, funding alerts, applications, etc.)

---

### **STEP 6: Set Up GitHub Actions** (3 minutes)

**Enable automated job scraping:**

1. Go to your forked repo on GitHub
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"

**Add these secrets one by one:**

```
Name: SUPABASE_URL
Value: (your Supabase Project URL)

Name: SUPABASE_KEY
Value: (your Supabase API Key)
```

**Optional (for better results):**

```
Name: ADZUNA_APP_ID
Value: (get from developer.adzuna.com - free)

Name: ADZUNA_API_KEY
Value: (get from developer.adzuna.com - free)

Name: REED_API_KEY
Value: (get from reed.co.uk/developers - free)
```

5. Click "Actions" tab
6. Click "I understand my workflows, go ahead and enable them"
7. ✅ Jobs will now scrape automatically every hour!

---

### **STEP 7: Test Your Site** (1 minute)

1. Visit your Vercel URL: `startup-scout-xxxxx.vercel.app`
2. Click "Sign Up"
3. Enter email and password
4. Complete onboarding (3 steps):
   - Select your background
   - Choose roles you want
   - Pick locations, salary, stage
5. ✅ You should see the dashboard with sample jobs!

**First scrape runs in 1 hour**, then you'll see real jobs from all 6 sources.

---

## ✅ You're Done!

**Your startup job platform is LIVE!** 🎉

**What happens now:**
- GitHub Actions runs every hour
- Scrapes 6 job sources
- Adds 20-50 new jobs
- You visit the site when you want
- Check NEWS tab for funding alerts
- Check JOBS tab for new jobs
- Apply to roles with <20 applicants

---

## 🎓 First Time User Guide

**When you first log in:**

1. **NEWS Tab:**
   - See funding announcements
   - Click "Watch" on companies that interest you
   - You'll be alerted when they post jobs

2. **JOBS Tab:**
   - Browse all jobs in spreadsheet view
   - Filter by source, stage, location
   - Sort by newest first
   - Apply to jobs with few applicants (🔴 NEW badge)

3. **TRACKING Tab:**
   - Drag & drop applications through pipeline
   - Track: Applied → Screening → Interview → Offer
   - Add notes per application

4. **SETTINGS Tab:**
   - Update job preferences
   - Manage watchlist
   - Configure notifications

---

## 🔧 Advanced Configuration

### Custom Domain (Optional - $10/year)

1. Buy domain from Namecheap/Google Domains
2. In Vercel: Settings → Domains → Add
3. Follow DNS instructions
4. ✅ Your site: `startupscout.com`

### Email Notifications (Optional)

1. Sign up at [resend.com](https://resend.com) (100 emails/day free)
2. Get API key
3. Add to Vercel environment variables:
   ```
   RESEND_API_KEY=re_xxxxx
   ```

### Crunchbase Funding Alerts (Optional - $50/month)

1. Sign up at [piloterr.com/crunchbase](https://piloterr.com/api/crunchbase)
2. Get API key
3. Add to Vercel environment variables:
   ```
   CRUNCHBASE_API_KEY=xxxxx
   ```

---

## 🐛 Troubleshooting

### "Jobs aren't loading"
- Check GitHub Actions: Go to repo → Actions tab
- See if scraper ran successfully
- If failed, check secrets are set correctly

### "Can't sign up"
- Check Supabase is running
- Go to Supabase → Settings → API
- Make sure "Allow anonymous sign-ins" is enabled

### "Database errors"
- Re-run database schema: Copy `database/schema.sql` → Supabase SQL Editor → Run
- Check Row Level Security is enabled

### "Scrapers not running"
- Check GitHub Actions is enabled: Repo → Settings → Actions → Allow all actions
- Check secrets are set: Repo → Settings → Secrets

---

## 📊 Monitoring

### Check Scraper Status

1. **GitHub Actions:** Repo → Actions tab
   - See each hourly run
   - View logs if failed

2. **Supabase:** Project → Table Editor
   - Check `jobs` table for new entries
   - Should grow by 20-50 rows/hour

3. **Vercel:** Project → Deployments
   - See deployment status
   - View analytics

---

## 🚀 Scaling Up

**Free tier supports:**
- 1000+ active users
- 10,000 jobs in database
- 100k pageviews/month

**When to upgrade:**
- >1000 users → Supabase Pro ($25/mo)
- >100k pageviews → Vercel Pro ($20/mo)
- >10k jobs → Need better search → Algolia ($0-29/mo)

---

## 🎯 API Keys Cheat Sheet

**Required (FREE):**
- ✅ Supabase URL + Key → Get from Supabase dashboard

**Optional but recommended (FREE):**
- Adzuna API → [developer.adzuna.com](https://developer.adzuna.com/)
- Reed API → [reed.co.uk/developers](https://www.reed.co.uk/developers)

**Optional for power users (PAID):**
- Crunchbase API → [$50/mo via Piloterr](https://piloterr.com)
- SendGrid → [Free for 100 emails/day](https://sendgrid.com)

---

## 📞 Need Help?

**Common issues:**
- [GitHub Issues](https://github.com/YOUR_USERNAME/startup-scout/issues)
- [Discussions](https://github.com/YOUR_USERNAME/startup-scout/discussions)

**Documentation:**
- [Vercel Docs](https://vercel.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## 🎉 Congratulations!

You now have a **fully automated startup job discovery platform** running for **$0/month**!

**Next steps:**
1. Share with friends looking for startup jobs
2. Customize the design (edit `frontend/index.html`)
3. Add more job sources
4. Build a community around it

**Star the repo ⭐ if you find it useful!**

---

**Happy job hunting! 🚀**
