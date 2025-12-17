# app.py
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)

# ====== 请在这里填写你的邮箱信息（用于接收订单）======
YOUR_EMAIL = "your_email@example.com"        # 比如：abc@gmail.com 或 163/qq 邮箱
EMAIL_PASSWORD = "your_smtp_password"        # 不是登录密码！是授权码（见下方说明）
SMTP_SERVER = "smtp.example.com"             # Gmail: smtp.gmail.com；QQ: smtp.qq.com；163: smtp.163.com
# ========================================================

@app.route("/")
def index():
    return render_template("order.html")

@app.route("/submit", methods=["POST"])
def submit_order():
    try:
        name = request.form.get("name", "匿名")
        phone = request.form.get("phone", "")
        cake = request.form.get("cake", "未选择")
        size = request.form.get("size", "8寸")
        message = request.form.get("message", "无")
        note = request.form.get("note", "")

        # 生成简洁订单
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        order_id = f"CAKE{hash(name + phone + order_time) % 10000:04d}"
        
        order_text = f"""
🎂 新蛋糕订单 #{order_id}
时间：{order_time}
姓名：{name}
电话：{phone}
蛋糕款式：{cake}
尺寸：{size}
祝福语：{message}
备注：{note}

👉 请让客户微信转账，并备注订单号：{order_id}
        """.strip()

        # 发送邮件通知你
        msg = MIMEText(order_text, "plain", "utf-8")
        msg["Subject"] = f"【新订单】#{order_id} - {name}"
        msg["From"] = YOUR_EMAIL
        msg["To"] = YOUR_EMAIL

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(YOUR_EMAIL, EMAIL_PASSWORD)
            server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg.as_string())

        return f"""
        <div style="text-align:center; padding:30px; font-family:sans-serif;">
            <h2>✅ 订单提交成功！</h2>
            <p>订单号：<strong>{order_id}</strong></p>
            <p>请用微信扫下方二维码付款，并<strong>备注订单号</strong>：</p>
            <img src="/static/wechat_pay_qr.jpg" width="220" style="border:1px solid #eee; border-radius:12px;">
            <p style="margin-top:20px; color:#666;">我们会尽快与您联系确认细节！</p>
            <a href="/" style="display:inline-block; margin-top:20px; color:white; background:#ff6b9d; padding:10px 20px; text-decoration:none; border-radius:6px;">再订一个</a>
        </div>
        """
    except Exception as e:
        return f"<h2>❌ 提交失败</h2><p>错误：{str(e)}</p><p>请截图并微信联系我手动下单。</p>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
