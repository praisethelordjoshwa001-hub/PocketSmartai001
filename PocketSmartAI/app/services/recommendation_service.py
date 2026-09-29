from app.services.catalog import HOME_CATALOG, PARTY_CATALOG, JEWELRY_CATALOG, search_url
from app.services.gemini_service import generate_recommendation

def _local_items(catalog, budget, count=6):
    chosen=[]; running=0
    for name, category, price, platform in sorted(catalog, key=lambda x:x[2]):
        if running + price <= budget * .92 or not chosen:
            chosen.append({"name":name,"category":category,"estimated_price":float(price),"platform":platform,
                "search_url":search_url(platform,name),"reason":"Practical option selected to keep the plan within the target budget.",
                "budget_share":round(price/budget*100,1)})
            running += price
        if len(chosen)>=count: break
    return chosen, running

def _normalise_ai(data,budget,planner):
    recs=[]; total=0
    for item in (data.get("recommendations") or [])[:10]:
        price=max(0,float(item.get("estimated_price",0))); total += price
        platform=item.get("platform") or "Amazon"; name=item.get("name") or "Recommended option"
        recs.append({"name":name,"category":item.get("category","General"),"estimated_price":price,"platform":platform,
            "search_url":search_url(platform,name),"reason":item.get("reason","Matches the stated preferences and budget."),
            "budget_share":round(price/budget*100,1) if budget else 0})
    return {"planner":planner,"title":data.get("title",f"{planner.title()} recommendations"),"summary":data.get("summary","Budget-aware recommendations generated for your plan."),
        "total_budget":budget,"estimated_total":round(total,2),"remaining_budget":round(budget-total,2),"tips":data.get("tips") or ["Keep a reserve for delivery, taxes and unexpected costs."],"recommendations":recs,"ai_powered":True}

def build_home(data):
    ai=generate_recommendation("home",data)
    if ai:return _normalise_ai(ai,data["budget"],"home")
    recs,total=_local_items(HOME_CATALOG,data["budget"])
    return {"planner":"home","title":"Smart Home Interior Plan","summary":f"A {data.get('style','Modern')} plan for {', '.join(data.get('rooms') or ['your home'])}.","total_budget":data["budget"],"estimated_total":round(total,2),"remaining_budget":round(data["budget"]-total,2),"tips":["Measure spaces before buying furniture.","Keep 8–10% as a contingency reserve."],"recommendations":recs,"ai_powered":False}

def build_party(data):
    ai=generate_recommendation("party",data)
    if ai:return _normalise_ai(ai,data["budget"],"party")
    recs,total=_local_items(PARTY_CATALOG,data["budget"]); per_guest=data["budget"]/max(1,data["guests"])
    return {"planner":"party","title":f"{data['event_type'].title()} Party Plan","summary":f"Estimated budget for {data['guests']} guests: ₹{data['budget']:,.0f} (₹{per_guest:,.0f}/guest).","total_budget":data["budget"],"estimated_total":round(total,2),"remaining_budget":round(data["budget"]-total,2),"tips":["Confirm guest count before final food orders.","Keep venue, food and decoration costs separate."],"recommendations":recs,"ai_powered":False}

def build_jewelry(data,image_bytes=None,mime_type=None):
    ai=generate_recommendation("jewelry",data,image_bytes,mime_type)
    if ai:return _normalise_ai(ai,data["budget"],"jewelry")
    recs,total=_local_items(JEWELRY_CATALOG,data["budget"]); color=data.get("outfit_color") or "your outfit color"
    return {"planner":"jewelry","title":f"{data['occasion'].title()} Jewelry Plan","summary":f"Style suggestions for a {data.get('style','Elegant')} look, considering {color}.","total_budget":data["budget"],"estimated_total":round(total,2),"remaining_budget":round(data["budget"]-total,2),"tips":["Match jewelry scale to the neckline and occasion.","Verify seller authenticity and current price before purchase."],"recommendations":recs,"ai_powered":False}
