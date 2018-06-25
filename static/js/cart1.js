  //选中数量的数组
        nums = [];
        ids = [];
        cars = [];
        $(function () {
            $("#buy_btn").click(function () {
                    /*jquery通过选择器定位到(已经被选择的数据)*/
                    let $sum_input = $('.order_content input:checked')
                        .parent()
                        .nextAll('.list_amount')
                        .find('.sum');
                    /*遍历选中input（checked已经被选中的）元素的数量*/
                    $sum_input.each(function () {
                        car = {
                            num: $(this).val(),
                            car_id: $(this).attr('id'),
                        };
                        /*将car对象放入列表*/
                        cars.push(car)

                    });
                    data = {
                        cars: JSON.stringify(cars),
                        csrfmiddlewaretoken: '{{ csrf_token }}

                    };
                    $.ajax({
                        url: '{% url 'buy' %}',
                        type: 'post',
                        data: data,
                        traditional: true,
                    })
                }
            )
        })
