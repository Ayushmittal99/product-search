from flask import Flask, request, jsonify, render_template_string
import amazon_research_final as agent
import os

app = Flask(__name__)

HTML_FORM = '''<!DOCTYPE html>
<html>
<head>
    <title>Amazon Research Agent</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        .form-group { margin: 16px 0; }
        label { display: block; font-weight: 500; margin-bottom: 6px; }
        input, textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; box-sizing: border-box; }
        button { padding: 10px 20px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
        button:hover { background: #0052a3; }
        #results { margin-top: 24px; padding: 16px; background: #f5f5f5; border-radius: 4px; white-space: pre-wrap; font-family: monospace; font-size: 12px; max-height: 400px; overflow-y: auto; }
        .loading { color: #666; font-style: italic; }
        .error { color: #d32f2f; }
        .success { color: #388e3c; }
    </style>
</head>
<body>
    <h1>Amazon Product Research Agent</h1>
    
    <form id="research-form">
        <div class="form-group">
            <label>Product Category *</label>
            <input type="text" name="category" placeholder="e.g. Kitchen gadgets" required>
        </div>
        
        <div class="form-group">
            <label>Min Price ($)</label>
            <input type="number" name="min_price" value="0" min="0" step="0.01">
        </div>
        
        <div class="form-group">
            <label>Max Price ($)</label>
            <input type="number" name="max_price" value="1000" min="0" step="0.01">
        </div>
        
        <div class="form-group">
            <label>Min Reviews</label>
            <input type="number" name="min_reviews" value="100" min="0">
        </div>
        
        <div class="form-group">
            <label>Min Rating</label>
            <input type="number" name="min_rating" value="3.5" min="0" max="5" step="0.1">
        </div>
        
        <button type="submit">Search Products</button>
    </form>
    
    <div id="results"></div>
    
    <script>
        document.getElementById('research-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const resultsDiv = document.getElementById('results');
            
            const formData = new FormData(e.target);
            const data = {
                category: formData.get('category'),
                min_price: parseFloat(formData.get('min_price')),
                max_price: parseFloat(formData.get('max_price')),
                min_reviews: parseInt(formData.get('min_reviews')),
                min_rating: parseFloat(formData.get('min_rating'))
            };
            
            resultsDiv.innerHTML = '<div class="loading">Searching...</div>';
            
            try {
                const response = await fetch('/research', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (!response.ok) {
                    resultsDiv.innerHTML = `<div class="error">Error: ${result.error}</div>`;
                    return;
                }
                
                resultsDiv.innerHTML = `<div class="success">Found ${result.count} products</div>\\n\\n${JSON.stringify(result.products, null, 2)}`;
            } catch (err) {
                resultsDiv.innerHTML = `<div class="error">Request failed: ${err.message}</div>`;
            }
        });
    </script>
</body>
</html>'''

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM)

@app.route("/research", methods=["POST"])
def research():
    data = request.json
    
    # data ko extract karega . 
    category = data.get("category")
    min_price = float(data.get("min_price", 0))
    max_price = float(data.get("max_price", 1000))
    min_reviews = int(data.get("min_reviews", 100))
    min_rating = float(data.get("min_rating", 3.5))
    
    if not category:
        return jsonify({"error": "category required"}), 400
    
    results = agent.run_research(category, min_price, max_price, min_reviews, min_rating)

    return jsonify({
        "count": len(results),
        "products": results
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)