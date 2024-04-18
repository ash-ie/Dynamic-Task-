from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
# Create your models here.
class BaseModel(models.Model):
    """Model for subclassing."""
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-created_on']

class UserManager(BaseUserManager):        
    def create_user(self, is_active=True,username=None,email=None, password=None,role=None, uid=None):
        
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=is_active, 
            role=role,
            uid=uid,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, email=None,role=None,uid=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            role=1,
            uid=uid,
            )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True 
        user.save(using=self._db)
        return user
    
SELECTROLE = ((1, "admin"), (2, "team_lead"), (3, "employee"))

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    email = models.EmailField(max_length=100, null=True)
    role = models.IntegerField(choices=SELECTROLE)
    uid = models.CharField(max_length=500, unique=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.username
    class Meta:
        db_table = "user"

class UserProfile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25,blank=True, null=True)
    mobile_number = models.CharField(max_length=25,unique=True, null=True)
    photo = models.ImageField(upload_to='images', blank=True, null=True)
    location = models.CharField(max_length=25,blank=True, null=True)
    position = models.CharField(max_length=50,blank=True, null=True)

class Project(BaseModel):
    teamlead = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    