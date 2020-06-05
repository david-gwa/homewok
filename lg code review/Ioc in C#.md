        

## to understand IoC  

using the example from [register and resolve in unity container](https://www.tutorialsteacher.com/ioc/register-and-resolve-in-unity-container)


```c#

public interface ICar
{
    int Run();
}

public class BMW : ICar
{
    private int _miles = 0;

    public int Run()
    {
        return ++_miles;
    }
}

public class Ford : ICar
{
    private int _miles = 0;

    public int Run()
    {
        return ++_miles;
    }
}

public class Driver
{
    private ICar _car = null;

    public Driver(ICar car)
    {
        _car = car;
    }

    public void RunCar()
    {
        Console.WriteLine("Running {0} - {1} mile ", _car.GetType().Name, _car.Run());
    }
}

```


the `Driver` class depends on `ICar` interface. so when instantiate the `Driver` class object, need to pass an instance of `ICar`, e.g.  BMW, Ford as following:

```c#

Driver driver = new Driver(new Ford());
driver.RunCar()

``` 


**to use IoC**, taking UnityContainer framework as example, a few other choices: TinyIoC e.t.c.

```c#

 var container = new UnityContainer();

```


* Register 

create an object of the `BMW` class and inject it through a constructor whenever you need to inject an ojbect of `ICar`.

```c#

container.Register<ICar, BMW>();
```

* Resolve

`Resolve` will create an object of the `Driver` class by automatically creating and njecting a `BMW` object in it, since previously register `BMW` type with `ICar`.


```c#

Driver  drv =  container.Resolve<Driver>();
drv.RunCar()

``` 

### summary 

there are two obvious advantages with IoC. 

* the instantiate of dependent class can be done in run time, rather during compile. e.g.  `ICar` class doesn't instantiate in `Driver` definition

* automatic `new class` management, without explit 





 
