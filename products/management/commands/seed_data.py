from django.core.management.base import BaseCommand

from products.models import Category, Product, ProductImage


def pic(seed, w=600, h=450):
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


DATA = {
    ("Rau củ", "rau-cu"): [
        ("Cà rốt Đà Lạt", "kg", 35000, 10, 120, "Cà rốt tươi giòn ngọt, trồng tại Đà Lạt."),
        ("Cà chua bi", "kg", 60000, 0, 80, "Cà chua bi đỏ mọng, ăn sống hoặc làm salad."),
        ("Bông cải xanh", "kg", 55000, 15, 60, "Bông cải xanh giàu vitamin C, không thuốc trừ sâu."),
        ("Khoai tây", "kg", 28000, 0, 200, "Khoai tây vàng, thích hợp chiên, nướng, hầm."),
        ("Dưa leo", "kg", 22000, 0, 140, "Dưa leo xanh giòn, mát, ăn sống hoặc muối chua."),
        ("Ớt chuông đỏ", "kg", 75000, 10, 50, "Ớt chuông đỏ ngọt, giàu vitamin, dùng xào hoặc salad."),
        ("Bắp cải trắng", "kg", 18000, 0, 160, "Bắp cải trắng cuốn chặt, ngọt, dùng nấu canh và xào."),
    ],
    ("Trái cây", "trai-cay"): [
        ("Xoài cát Hòa Lộc", "kg", 90000, 5, 70, "Xoài cát thơm ngọt, thịt dày, ít xơ."),
        ("Cam sành", "kg", 45000, 0, 150, "Cam sành mọng nước, nhiều vitamin C."),
        ("Chuối già", "kg", 25000, 0, 100, "Chuối già chín tự nhiên, ngọt dịu."),
        ("Dưa hấu không hạt", "kg", 30000, 20, 5, "Dưa hấu đỏ ruột, ngọt mát, không hạt."),
        ("Dâu tây Đà Lạt", "hộp", 180000, 12, 30, "Dâu tây đỏ mọng, chua ngọt, hộp 500g."),
        ("Nho xanh không hạt", "kg", 120000, 10, 40, "Nho xanh giòn ngọt, không hạt, nhập khẩu."),
        ("Thanh long ruột đỏ", "kg", 48000, 0, 90, "Thanh long ruột đỏ ngọt đậm, nhiều nước."),
    ],
    ("Đồ uống", "do-uong"): [
        ("Cà phê rang xay", "gói", 120000, 10, 90, "Cà phê Robusta rang xay nguyên chất 500g."),
        ("Trà ô long", "hộp", 150000, 0, 45, "Trà ô long thơm dịu, hộp 200g."),
        ("Nước ép cam", "chai", 32000, 0, 100, "Nước ép cam nguyên chất 330ml ."),
        ("Nước dừa tươi", "chai", 25000, 0, 110, "Nước dừa xiêm tươi, đóng chai 500ml."),
        ("Trà xanh không độ", "chai", 12000, 0, 250, "Trà xanh đóng chai 455ml, vị thanh mát."),
        ("Nước khoáng thiên nhiên", "thùng", 85000, 5, 70, "Thùng 24 chai nước khoáng 500ml."),
    ],
    ("Đồ khô", "do-kho"): [
        ("Gạo ST25", "kg", 32000, 0, 300, "Gạo thơm ST25 đạt giải gạo ngon nhất thế giới."),
        ("Hạt điều rang muối", "gói", 185000, 12, 60, "Hạt điều Bình Phước rang muối, gói 500g."),
        ("Mì gói hảo hảo", "thùng", 115000, 0, 80, "Thùng 30 gói mì tôm chua cay."),
        ("Đậu phộng rang", "gói", 45000, 0, 120, "Đậu phộng rang giòn, gói 300g."),
    ],
    ("Thịt & Hải sản", "thit-hai-san"): [
        ("Thịt ba chỉ heo", "kg", 135000, 0, 40, "Thịt ba chỉ heo tươi, nhiều nạc, thích hợp kho và nướng."),
        ("Ức gà phi lê", "kg", 98000, 5, 50, "Ức gà phi lê không xương, ít mỡ, tốt cho người tập thể thao."),
        ("Thịt bò Úc", "kg", 320000, 10, 25, "Thịt bò nhập khẩu từ Úc, mềm, thích hợp làm bít tết."),
        ("Cá hồi phi lê", "kg", 420000, 8, 20, "Cá hồi Na Uy phi lê tươi, giàu omega-3."),
        ("Tôm thẻ tươi", "kg", 210000, 0, 35, "Tôm thẻ tươi size vừa, thịt chắc ngọt."),
    ],
    ("Sữa & Trứng", "sua-trung"): [
        ("Sữa tươi không đường", "hộp", 32000, 0, 120, "Sữa tươi tiệt trùng không đường, hộp 1 lít."),
        ("Sữa chua có đường", "lốc", 28000, 0, 90, "Lốc 4 hũ sữa chua có đường."),
        ("Trứng gà ta", "vỉ", 45000, 0, 80, "Vỉ 10 quả trứng gà ta, lòng đỏ đậm."),
        ("Phô mai lát", "gói", 58000, 10, 60, "Phô mai lát tan chảy, gói 10 lát."),
    ],
    ("Bánh kẹo", "banh-keo"): [
        ("Bánh quy bơ", "hộp", 65000, 15, 100, "Bánh quy bơ giòn thơm, hộp thiếc 400g."),
        ("Kẹo dừa Bến Tre", "gói", 35000, 0, 150, "Kẹo dừa dẻo thơm béo, đặc sản Bến Tre."),
        ("Socola đen 70%", "thanh", 48000, 0, 70, "Socola đen 70% cacao, vị đắng nhẹ."),''
        ("Snack khoai tây", "gói", 18000, 0, 200, "Snack khoai tây giòn tan, vị tự nhiên."),
    ],
    ("Gia vị", "gia-vi"): [
        ("Nước mắm Phú Quốc", "chai", 55000, 0, 110, "Nước mắm cá cơm Phú Quốc 40 độ đạm, chai 500ml."),
        ("Muối tôm Tây Ninh", "hũ", 22000, 0, 130, "Muối tôm Tây Ninh cay mặn, chấm trái cây rất ngon."),
        ("Tiêu đen xay", "hũ", 40000, 10, 85, "Tiêu đen xay thơm nồng, hũ 100g."),
        ("Dầu ăn đậu nành", "chai", 52000, 0, 95, "Dầu ăn đậu nành nguyên chất, chai 1 lít."),
    ],
}


class Command(BaseCommand):
    help = "Nạp danh mục, sản phẩm và ảnh mẫu"

    def handle(self, *args, **options):
        n_cat = n_prod = 0
        for (cname, slug), items in DATA.items():
            cat, created = Category.objects.get_or_create(slug=slug, defaults={"name": cname})
            n_cat += created
            for name, unit, price, discount, amount, desc in items:
                prod, created = Product.objects.update_or_create(
                    name=name, category_id=cat,
                    defaults=dict(unit=unit, price=price, discount=discount, amount=amount,
                                  description=desc, thumbnail=pic(slug + "-" + str(len(name)) + name[:3])),
                )
                if created:
                    n_prod += 1
                    for i in (1, 2):
                        ProductImage.objects.create(product_id=prod, image_url=pic(f"p{prod.id}-{i}"))
        self.stdout.write(self.style.SUCCESS(f"Đã thêm {n_cat} danh mục mới, {n_prod} sản phẩm mới."))