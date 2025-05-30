# README - Project Management API


في هذا التحديث، قمت بتطوير وتحسين API لإدارة المشاريع ومهامها  باستخدام Django REST Framework، وشملت الرئيسية:

- إنشاء `TaskViewSet` لدعم عمليات CRUD كاملة المشاريع.
- إنشاء `TaskViewSet` لدعم عمليات CRUD كاملة للمهام.
- تطبيق صلاحيات مخصصة باستخدام Permission Classes مثل:
  - `IsAdminUser`
  - `Project Permissions`
  - -  `IsProjectManager`
  - -`IsAdminOrProjectManager`
  - -`IsAdminOrProjectManagerOrMember`
  - `Task Permissions`
  - -`IsTaskAssignee`
  - -`IsProjectManagerOfTask`
  - -`IsAdminOrProjectManagerOrTaskAssignee`

  -  لتحديد صلاحيات الوصول حسب دور المستخدم.
- إضافة عدة projects endpoints خاصة منها:
  - إنشاء مشروع جديد (Admin فقط)
  - عرض قائمة المشاريع كل مستخدم يعرض المشاريع فقط الذي هو مديرها او عضو فيها
  - عرض تفاصيل مشروع معين
  - تحديث مشروع (Admin أو مدير مشروع)
  - حذف مشروع (Admin أو مدير مشروع)
  - إضافة عضو للمشروع (Admin أو مدير مشروع)
  - إزالة عضو من المشروع (Admin أو مدير مشروع)
 - إضافة عدة projects endpoints خاصة منها:
  - عرض كل مهام مشروع معين	من ضمن مشاريعي ك مستخدم
  - إنشاء مهمة جديدة (Admin أو مدير مشروع)
  - عرض تفاصيل مهمة معينة
  - تحديث مهمة (Admin أو مدير مشروع او العضو المكلف بها)
  - تكليف عضو بمهمة (Admin او مدير مشروع فقط)
  -  
- دعم الفلترة والبحث باستخدام `DjangoFilterBackend` و `TaskFilter`.
- استخدام `DefaultRouter` لتنظيم الراوتات.

## كيفية اختبار الـ API

يمكنك اختبار جميع الـ endpoints بسهولة باستخدام **Postman**.

### خطوات الاختبار:

1. افتح برنامج Postman.
2. استورد ملف **Postman Collection** المرفق (`YasmeenAi_training_task5.postman_collection.json`) عبر:  
   `File` -> `Import` -> اختر ملف الـ JSON.
3. قم بضبط إعدادات **Authorization** لكل طلب إذا كانت مطلوبة (مثلاً إضافة JWT Token في الـ Headers).
4. جرب تنفيذ الطلبات (GET, POST, PUT, DELETE) حسب الـ endpoint.
5. راقب الردود والنتائج من السيرفر.

---

> **ملاحظة:**  
> تم ارفاق ملف ال Postman Collection على رابط تقديم التاسك

---
